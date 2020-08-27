# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import argparse
import datetime
from collections import namedtuple

import h5py

from gomoku import agents
from gomoku import rl
from gomoku.utils import print_board
from gomoku.types import Player, Point
from gomoku.board import GameState

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, required=True)
    parser.add_argument('--learning-agent', required=True)
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--experience-out', required=True)

    args = parser.parse_args()
    agent_filename = args.learning_agent
    experience_filename = args.experience_out
    global BOARD_SIZE
    BOARD_SIZE = args.board_size

    agent1 = agents.pg.load_policy_agent(h5py.File(agent_filename))
    agent2 = agents.pg.load_policy_agent(h5py.File(agent_filename))
    collector1 = rl.ExperienceCollector()
    collector2 = rl.ExperienceCollector()
    agent1.set_collector(collector1)
    agent2.set_collector(collector2)

    for i in range(args.num_games):
        print(f'Simulating game {i+1}/{args.num_games}...')
        collector1.begin_episode()
        collector2.begin_episode()

        game_record = simulate_game(agent1, agent2)
        if game_record.winner == Player.black:
            collector1.complete_episode(reward=1)
            collector2.complete_episode(reward=-1)
        else:
            collector2.complete_episode(reward=1)
            collector1.complete_episode(reward=-1)

    experience = rl.combine_experience([collector1, collector2])
    with h5py.File(experience_filename, 'w') as experience_outf:
        experience.serialize(experience_outf)

if __name__ == '__main__':
    main()