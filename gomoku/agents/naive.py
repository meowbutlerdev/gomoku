# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import random
from gomoku.agents.base import Agent
from gomoku.board import Move
from gomoku.types import Point

class RandomBot(Agent):
    def select_move(self, game_state):
        # 임의의 유효한 수를 선택한다.
        candidates = []
        for row in range(game_state.board.num_rows):
            for col in range(game_state.board.num_cols):
                candidate = Point(row=row+1, col=col+1)
                if game_state.is_valid_move(Move.play(candidate)):
                    candidates.append(candidate)
        return Move.play(random.choice(candidates))