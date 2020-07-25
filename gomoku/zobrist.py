# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import random
from gomoku.types import Player, Point

__all__ = ['HASH_CODE', 'EMPTY_BOARD']

def to_python(player_state):
    if player_state is None:
        return 'None'
    if player_state == Player.black:
        return Player.black
    return Player.white

MAX63 = 0x7fffffffffffffff

table = {}
empty_board = random.randint(0, MAX63)
for row in range(1, 20):
    for col in range(1, 20):
        for state in (None, Player.black, Player.white):
            code = random.randint(0, MAX63)
            table[Point(row, col), state] = code

temp = ['HASH_CODE = {',]
for (pt, state), hash_code in table.items():
    temp.append(f'({pt}, {str(to_python(state))}): {hash_code},')
temp.append('}')

exec("\n".join(temp))
exec(f'EMPTY_BOARD = {empty_board}')