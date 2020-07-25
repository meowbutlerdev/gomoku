# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from gomoku import types

# 바둑판 열 번호 정의
COLS = 'ABCDEFGHJKLMNOPQRST'
# 바둑판 돌 표시
STONE_TO_CHAR = {
    None: ' . ',
    types.Player.black: ' X ',
    types.Player.white: ' O '
}

# 돌 착수 위치 출력
def print_move(player, move):
    move_str = f'{COLS[move.point.col - 1]}{move.point.row}'
    print(f'{str(player)} {move_str}')

# 바둑판 출력
def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = ' ' if row <= 9 else ''
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(types.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print(f'{bump}{row} {"".join(line)}')
    print(f'{"    "}{"  ".join(COLS[:board.num_cols])}')

# 사람의 입력값을 좌표로 변환
def point_from_coords(coords):
    col = COLS.index(coords[0].upper()) + 1
    row = int(coords[1:])
    return types.Point(row=row, col=col)