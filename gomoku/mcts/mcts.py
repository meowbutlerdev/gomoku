# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import math
import random
from gomoku import agent
from gomoku.types import Player

# MCTS 롤아웃
class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        # 현재 노드에서의 대국 상태
        self.game_state = game_state
        # 현재 노드의 부모 노드
        # 대국이 처음 시작될 때의 parent는 None
        self.parent = parent
        # 현재 노드의 마지막 수
        # 이 함수의 결과를 새로운 노드에 저장하고, 그 노드의 모든 조상에 반영
        self.move = move
        # 현재 노드에서의 롤아웃 결과
        self.win_counts = {
            Player.black: 0,
            Player.white: 0,
        }
        self.num_rollouts = 0
        # 현재 노드에서 가능한 경우의 수 리스트
        # 새로운 노드가 추가될 때마다 이 리스트에서 하나를 선택하고, 그에 대한 MCTSNode를 생성하여 children 리스트에 추가한다.
        self.children = []
        self.unvisited_moves = game_state.legal_moves()

    # MCTS 트리에 새로운 노드 추가
    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    # 롤아웃 통계 갱신
    def record_win(self, winner):
        if winner is None:
            self.win_counts[Player.black] += 1
            self.win_counts[Player.white] += 1
        else:
            self.win_counts[winner] += 1
        self.num_rollouts += 1

    # 현재 노드에서 가능한 수가 있는지 확인
    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    # 현재 노드에서 대국이 끝났는지 확인
    def is_terminal(self):
        return self.game_state.is_over()

    # 롤아웃 결과 이길 확률 확인
    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)

# MCTS 알고리즘
class MCTSAgent(agent.Agent):
    def __init__(self, num_rounds, temperature):
        agent.Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature

    # 다음 착수 점 선택
    def select_move(self, game_state):
        COLS = 'ABCDEFGHJKLMNOPQRST'
        root = MCTSNode(game_state)

        for _ in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            # 트리에 새로운 노드 추가
            if node.can_add_child():
                node = node.add_random_child()

            # 랜덤 게임 시뮬레이션
            winner = self.simulate_random_game(node.game_state)

            # 역전파
            while node is not None:
                node.record_win(winner)
                node = node.parent

        moves = []
        for child in root.children:
            moves.append(
                (
                    child.winning_frac(game_state.next_player),
                    child.move.point,
                    child.num_rollouts
                )
            )
        moves.sort(key=lambda x: x[0], reverse=True)
        for w, p, n in moves[:10]:
            print(f'{COLS[p.col-1]}{p.row} : {w*100:.1f}%({n}승)')

        # 승률이 가장 높은 수 선택
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        best_row, best_col = best_move.point.row, best_move.point.col
        print(f'승률 {best_pct*100:.1f}% {COLS[best_col-1]}{best_row} 선택')
        return best_move

    # UCT에 따른 자식노드 선택
    def select_child(self, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        for child in node.children:
            # UCT 계산
            win_percentage = child.winning_frac(node.game_state.next_player)
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor

            # UCT가 가장 큰 자식노드 선택
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    # 랜덤 게임 시뮬레이션
    @staticmethod
    def simulate_random_game(game):
        bots = {
            Player.black: agent.RandomBot(),
            Player.white: agent.RandomBot(),
        }
        while not game.is_over():
            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)

        if game.winner == 'Player.black':
            return Player.black
        elif game.winner == 'Player.white':
            return Player.white
        else:
            return None