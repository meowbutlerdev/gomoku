# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from gomoku import board
from gomoku import types
from gomoku import mcts
from gomoku.utils import print_board, print_move, point_from_coords

def main():
    board_size = 5
    game = board.GameState.new_game(board_size)
    bot = mcts.MCTSAgent(num_rounds=500, temperature=0.8)

    while not game.is_over():
        try:
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

        except ValueError:
            print('정확한 좌표를 입력하세요.')
        except IndexError:
            print('정확한 좌표를 입력하세요.')
        except AssertionError:
            print('이미 돌이 존재합니다.')

if __name__ == '__main__':
    main()