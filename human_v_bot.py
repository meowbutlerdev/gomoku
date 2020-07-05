# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from omok import agent
from omok import board
from omok import types
from omok.utils import print_board, print_move, point_from_coords

def main():
    board_size = 9
    game = board.GameState.new_game(board_size)
    bot = agent.RandomBot()

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

            game = game.apply_move(move)
            print_move(game.next_player, move)
        except ValueError:
            print('정확한 좌표를 입력하세요.')
        except IndexError:
            print('정확한 좌표를 입력하세요.')
        except AssertionError:
            print('이미 돌이 존재합니다.')

    print(f'{chr(27)}[2J')
    print_board(game.board)

    if game.winner is None:
        print('무승부!')
    else:
        print(f'{str(game.winner)}의 승리!')

if __name__ == '__main__':
    main()