# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import copy
from gomoku.types import Player, Point
from gomoku import zobrist

# 자기 차례에 할 수 있는 행동 정의 클래스
class Move():
    def __init__(self, point=None):
        assert (point is not None)
        self.point = point
        self.is_play = (self.point is not None)

    # 바둑판에 돌을 놓는 행동
    @classmethod
    def play(cls, point):
        return Move(point=point)

# 바둑판 정의 클래스
class Board():
    # 열과 행 수를 이용하여 바둑판 초기화
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = [[None for _ in range(num_rows + 1)] for _ in range(num_cols + 1)]
        self._hash = zobrist.EMPTY_BOARD

    # 착수
    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid[point.row][point.col] is None
        self._grid[point.row][point.col] = player
        self._hash ^= zobrist.HASH_CODE[point, player]

    # 점이 바둑판 내에 존재하는지 확인
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
               1 <= point.col <= self.num_cols

    # 만약 돌이 놓여있으면 Player를 반환하고,
    # 놓여있지 않으면 None을 반환
    def get(self, point):
        string_color = self._grid[point.row][point.col]
        return string_color

    # 현재 zobrist hash 값 반환
    def zobrist_hash(self):
        return self._hash

# 게임 현황 정의 클래스
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states |
                {(previous.next_player, previous.board.zobrist_hash())}
            )
        self.last_move = move
        self.winner = None

    # 착수 후 새로운 GameState 반환
    def apply_move(self, move):
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(self.next_player, move.point)
        return GameState(next_board, self.next_player.other, self, move)

    # 새로운 게임 생성
    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    # 돌이 5개 모였는지 확인
    def is_five(self, row, col):
        row = row
        col = col
        five = True

        # 현재 위치에서 우측 확인
        for i in range(1, 5):
            if not self.board.is_on_grid(Point(row=row, col=col+i)) or \
                   self.board._grid[row][col] != self.board._grid[row][col+i]:
                five = False
                break
        if five:
            return self.board._grid[row][col]
        else:
            five = True

        # 현재 위치에서 하단 확인
        for i in range(1, 5):
            if not self.board.is_on_grid(Point(row=row+i, col=col)) or \
                   self.board._grid[row][col] != self.board._grid[row+i][col]:
                five = False
                break
        if five:
            return self.board._grid[row][col]
        else:
            five = True

        # 현재 위치에서 좌하단 확인
        for i in range(1, 5):
            if not self.board.is_on_grid(Point(row=row+i, col=col-i)) or \
                   self.board._grid[row][col] != self.board._grid[row+i][col-i]:
                five = False
                break
        if five:
            return self.board._grid[row][col]
        else:
            five = True

        # 현재 위치에서 우하단 확인
        for i in range(1, 5):
            if not self.board.is_on_grid(Point(row=row+i, col=col+i)) or \
                   self.board._grid[row][col] != self.board._grid[row+i][col+i]:
                five = False
                break
        if five:
            return self.board._grid[row][col]

        return None

    # 대국이 종료되었는지 확인
    def is_over(self):
        is_board_full = True
        for row in range(self.board.num_rows):
            for col in range(self.board.num_cols):
                if self.board._grid[row+1][col+1] is not None:
                    winner = self.is_five(row+1, col+1)
                    if winner is not None:
                        self.winner = str(winner)
                        return True
                else:
                    is_board_full = False
        if is_board_full:
            self.winner = None
            return True
        else:
            return False

    # 현재 상태에서 유효한 수인지 확인
    def is_valid_move(self, move):
        return not self.board.get(move.point)

    # 현재 상태에서 유효한 수들 모음
    def legal_moves(self):
        moves = []
        for row in range(self.board.num_rows):
            for col in range(self.board.num_cols):
                move = Move.play(Point(row+1, col+1))
                if self.is_valid_move(move):
                    moves.append(move)

        return moves