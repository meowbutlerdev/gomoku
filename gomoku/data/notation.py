# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

class Gomoku_game:
    def __init__(self):
        self.cnt = 0

    def make_color(self, point):
        if '-' not in point:
            row = ord(point[0]) - 96
            col = point[1:]

            color = 'W' if self.cnt % 2 else 'B'
            move = (row, int(col))
            self.cnt += 1
            return color, move
        else:
            return None

    def from_string(self, data):
        notation = list(map(self.make_color, data))

        if None in notation:
            return None
        return notation