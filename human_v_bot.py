# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from omok import agent
from omok import board
from omok import types
from omok.utils import print_board, print_move, point_from_coords
from six.moves import input

def main():
    board_size = 9
    game = board.GameState.new_game(board_size)
    bot = agent.RandomBot()

    while not game.is_over():
        # 새로운 수를 둘 때마다 콘솔창 초기화
        print(f'{chr(27)}[2J')
        print_board(game.board)
        if game.next_player == types.Player.black:
            human_move = input('착수 : ')
            point = point_from_coords(human_move.strip())
            move = board.Move.play(point)
        else:
            move = bot.select_move(game)

        print_move(game.next_player, move)
        game = game.apply_move(move)

if __name__ == '__main__':
    main()