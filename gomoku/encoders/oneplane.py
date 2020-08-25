# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import numpy as np
from gomoku.encoders.base import Encoder
from gomoku.board import Point

class OnePlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):
        return 'oneplane'

    # 해당 점에 자신의 돌이 놓여있다면 1, 상대의 돌이 놓여있다면 -1, 빈 점은 0
    def encode(self, game_state):
        board_matrix = np.zeros(self.shape())
        next_player = game_state.next_player
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = Point(row=r + 1, col=c + 1)
                gomoku_string = game_state.board.get(p)
                if gomoku_string is None:
                    continue
                board_matrix[0, r, c] = 1 if gomoku_string == next_player else -1
            return board_matrix

    # 바둑판의 각 점들을 정수형 인덱스로 변환
    def encode_point(self, point):
        return self.board_width * (point.row - 1) + (point.col - 1)

    # 정수형 인덱스를 바둑판의 점으로 변환
    def decode_point_index(self, index):
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width

def create(board_size):
    return OnePlaneEncoder(board_size)