# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import h5py

from gomoku.agents import pg
from gomoku import rl
from gomoku import board
from gomoku import types

BOARD_SIZE = 9

def simulate_game(black_player, white_player):
    game = board.GameState.new_game(BOARD_SIZE)
    agents = {
        types.Player.black: black_player,
        types.Player.white: white_player
    }

    while not game.is_over():
        next_move = agents[game.next_player].select_move(game)
        game = game.apply_move(next_move)

    if game.winner is None:
        print('무승부!')
    else:
        print(f'{str(game.winner)}의 승리!')

agent1 = pg.load_policy_agent(h5py.File(agent_filename))
agent2 = pg.load_policy_agent(h5py.File(agent_filename))
collector1 = rl.ExperienceCollector()
collector2 = rl.ExperienceCollector()
agent1.set_collector((collector1))
agent2.set_collector((collector2))

num_games = 10
experience_filename = './agents/pg.hdf5'

for i in range(num_games):
    collector1.begin_episode()
    collector2.begin_episode()

    game_record = simulate_game(agent1, agent2)
    # agent1이 이겼을 경우 보상
    if game_record.winner == Player.black:
        collector1.complete_episode(reward=1)
        collector2.complete_episode(reward=-1)
    # agent2가 이겼을 경우 보상
    else:
        collector1.complete_episode(reward=-1)
        collector2.complete_episode(reward=1)

experience = rl.combine_experience(
    [
        collector1,
        collector2
    ]
)
with h5py.File(experience_filename, 'w') as experience_outf:
    experience.serialize(experience_outf)