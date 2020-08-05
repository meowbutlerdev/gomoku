# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import random
from gomoku.agent.base import Agent
from gomoku.board import Move
from gomoku.types import Point

class RandomBot(Agent):
    def select_move(self, game_state):
        # 임의의 유효한 수를 선택한다.
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)):
                    candidates.append(candidate)
        return Move.play(random.choice(candidates))