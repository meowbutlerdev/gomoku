# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from omok import agent
from omok import board
from omok import types
from omok.utils import print_board, print_move
import time

def main():
    board_size = 9
    game = board.GameState.new_game(board_size)
    bots = {
        types.Player.black: agent.naive.RandomBot(),
        types.Player.white: agent.naive.RandomBot()
    }

    while not game.is_over():
        time.sleep(0.3)

        # 새로운 수를 둘 때마다 콘솔창 초기화
        print(f'{chr(27)}[2J')
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)

if __name__ == '__main__':
    main()