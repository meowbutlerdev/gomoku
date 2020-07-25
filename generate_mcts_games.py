# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import argparse
import numpy as np

from gomoku.encoders import get_encoder_by_name
from gomoku import board
from gomoku import mcts
from gomoku.utils import print_board, print_move

# MCTS 대국 생성
# boards에는 바둑판의 현재 상태를 기록
# moves에는 수의 값을 변환하여 기록
def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []

    # OnePlaneEncoder에 이름과 바둑판 크기를 지정
    encoder = get_encoder_by_name('oneplane', board_size)

    # board_size 크기의 대국 초기화
    game = board.GameState.new_game(board_size)

    # 횟수와 온도가 정해진 몬테카를로 트리 탐색 에이전트
    bot = mcts.MCTSAgent(rounds, temperature)

    num_moves = 0
    while not game.is_over():
        print_board(game.board)
        # 봇이 다음 수 선택
        move = bot.select_move(game)
        if move.is_play:
            # 현재 대국 현황을 변환하여 boards에 추가
            boards.append(encoder.encode(game))

            # 원-핫 인코딩
            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            # 원-핫 인코딩된 다음 수를 moves에 추가
            moves.append(move_one_hot)

            print_move(game.next_player, move)
            # 봇이 선택한 다음 수를 착수
            game = game.apply_move(move)
            num_moves += 1
            # 정해진 최대 수만큼 반복
            if num_moves > max_moves:
                break

        return np.array(boards), np.array(moves)

# 예를 들어, 명령줄에서 아래와 같은 옵션을 사용하면 9x9 크기의 바둑판에 20개의 대국을 진행하고
# feature 데이터는 features.npy에 label 데이터는 labels.npy에 저장한다.
# python generate_mcts_game.py -n 20 --board-out features.npy --move-out labels.npy
def main():
    parser = argparse.ArgumentParser()
    # 바둑판 크기 옵션
    parser.add_argument('--board-size', '-b', type=int, default=9)
    # 대국 수 옵션
    parser.add_argument('--rounds', '-r', type=int, default=1000)
    # 온도 옵션
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    # 최대 착수 수 옵션
    parser.add_argument('--max-moves', '-m', type=int, default=60, help='Max moves per game.')
    # 최대 대국 수 옵션
    parser.add_argument('--num-games', '-n', type=int, default=10)
    # feature 파일명
    parser.add_argument('--board-out')
    # label 파일명
    parser.add_argument('--move-out')

    # 명령줄 인수를 통해 사용자별로 수정 허용
    args = parser.parse_args()
    xs, ys = [], []

    for i in range(args.num_games):
        print(f'Generating game {i + 1}/{args.num_games}')
        # 정해진 대국 수만큼 데이터 생성
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)

    # 모든 데이터 생성 후 feature와 label 결합
    x = np.concatenate(xs)
    y = np.concatenate(ys)

    # 명령줄에 입력된 파일명에 따라 각 파일에 feature와 label 저장
    np.save(args.board_out, x)
    np.save(args.move_out, y)

if __name__ == '__main__':
    main()