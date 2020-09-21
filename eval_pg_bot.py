# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import argparse
import datetime
from collections import namedtuple

import h5py

from gomoku import agents
from gomoku.utils import print_board
from gomoku.types import Player, Point
from gomoku.board import GameState

BOARD_SIZE = 15

def avg(items):
    if not items:
        return 0.0
    return sum(items) / float(len(items))

class GameRecord(namedtuple('GameRecord', 'moves winner')):
    pass

def name(player):
    if player == Player.black:
        return 'B'
    return 'W'

def simulate_game(black_player, white_player):
    moves = []
    game = GameState.new_game(BOARD_SIZE)
    agents = {
        Player.black: black_player,
        Player.white: white_player,
    }
    while not game.is_over():
        next_move = agents[game.next_player].select_move(game)
        moves.append(next_move)
        game = game.apply_move(next_move)

    print_board(game.board)
    print(game.winner)

    return GameRecord(
        moves=moves,
        winner=game.winner,
    )

def main():
    """example :
    python self_play_pg.py --agent1 <path> --agent2 <path> --num-games 100
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent1', required=True)
    parser.add_argument('--agent2', required=True)
    parser.add_argument('--num-games', '-n', type=int, default=10)

    args = parser.parse_args()

    agent1 = agents.pg.load_policy_agent(h5py.File(args.agent1))
    agent2 = agents.pg.load_policy_agent(h5py.File(args.agent2))

    # agent1의 관점에서 승패 추적
    wins = 0
    losses = 0
    # color1은 agent1의 색
    color1 = Player.black
    for i in range(args.num_games):
        print(f'Simulating game {i+1}/{args.num_games}...')
        if color1 == Player.black:
            black_player, white_player = agent1, agent2
        else:
            white_player, black_player = agent1, agent2
        game_record = simulate_game(black_player, white_player)
        if game_record.winner == str(color1):
            wins += 1
        else:
            losses += 1
        # 각 경기 종료 후 색을 바꿔서 어떤 에이전트가 특정 색에서 성능이 좋은지 확인
        color1 = color1.other
    print(f'Agent 1 record: {wins}/{wins+losses}')

if __name__ == '__main__':
    main()