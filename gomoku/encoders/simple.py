# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import numpy as np

from gomoku.encoders.base import Encoder
from gomoku.board import Move
from gomoku.types import Player, Point

# 10차 평면 변환기
# 0 - 1 : 흑과 백의 열린 3
# 2 - 3 : 흑과 백의 열린 4
# 4 - 5 : 흑과 백의 닫힌 3
# 6 - 7 : 흑과 백의 닫힌 4
# 8 : 흑의 턴일 때 1로 채움
# 9 : 백의 턴일 때 1로 채움
class SimpleEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 10

    def name(self):
        return 'simple'

    def encode(self, game_state):
        board_tensor = np.zeros(self.shape())
        if game_state.next_player == Player.black:
            board_tensor[8] = 1
        else:
            board_tensor[9] = 1

        for r in range(self.board_height):
            for c in range(self.board_width):
                open_closeds = game_state.open_closed(r+1, c+1)
                for ds, oc, s, d, cnt in open_closeds:
                    for i in range(len(d)):
                        if oc == 'open' and ds == 'right':
                            if s == Player.black:
                                board_tensor[0 if cnt == 3 else 2, r, c+i] = 1 if s == d[i] else 0
                            else:
                                board_tensor[1 if cnt == 3 else 3, r, c+i] = 1 if s == d[i] else 0
                        if oc == 'open' and ds == 'bottom':
                            if s == Player.black:
                                board_tensor[0 if cnt == 3 else 2, r+i, c] = 1 if s == d[i] else 0
                            else:
                                board_tensor[1 if cnt == 3 else 3, r+i, c] = 1 if s == d[i] else 0
                        if oc == 'open' and ds == 'bottom_left':
                            if s == Player.black:
                                board_tensor[0 if cnt == 3 else 2, r+i, c-i] = 1 if s == d[i] else 0
                            else:
                                board_tensor[1 if cnt == 3 else 3, r+i, c-i] = 1 if s == d[i] else 0
                        if oc == 'open' and ds == 'bottom_right':
                            if s == Player.black:
                                board_tensor[0 if cnt == 3 else 2, r+i, c+i] = 1 if s == d[i] else 0
                            else:
                                board_tensor[1 if cnt == 3 else 3, r+i, c+i] = 1 if s == d[i] else 0
                        if oc == 'closed' and ds == 'right':
                            if s == Player.black:
                                board_tensor[4 if cnt == 3 else 6, r, c+i] = 1 if s == d[i] else 0
                            else:
                                board_tensor[5 if cnt == 3 else 7, r, c+i] = 1 if s == d[i] else 0
                        if oc == 'closed' and ds == 'bottom':
                            if s == Player.black:
                                board_tensor[4 if cnt == 3 else 6, r+i, c] = 1 if s == d[i] else 0
                            else:
                                board_tensor[5 if cnt == 3 else 7, r+i, c] = 1 if s == d[i] else 0
                        if oc == 'closed' and ds == 'bottom_left':
                            if s == Player.black:
                                board_tensor[4 if cnt == 3 else 6, r+i, c-i] = 1 if s == d[i] else 0
                            else:
                                board_tensor[5 if cnt == 3 else 7, r+i, c-i] = 1 if s == d[i] else 0
                        if oc == 'closed' and ds == 'bottom_right':
                            if s == Player.black:
                                board_tensor[4 if cnt == 3 else 6, r+i, c+i] = 1 if s == d[i] else 0
                            else:
                                board_tensor[5 if cnt == 3 else 7, r+i, c+i] = 1 if s == d[i] else 0
        return board_tensor

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
    return SimpleEncoder(board_size)