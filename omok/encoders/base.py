# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import importlib

# 변환기
class Encoder:
    # 변환기 이름 로깅 혹은 저장
    def name(self):
        raise NotImplementedError()

    # 바둑판 현재 상태를 숫자로 변환
    def encode(self, game_state):
        raise NotImplementedError()

    # 바둑판의 각 점들을 정수형 인덱스로 변환
    def encode_point(self, point):
        raise NotImplementedError()

    # 정수형 인덱스를 바둑판의 점으로 변환
    def decode_point_index(self, index):
        raise NotImplementedError()

    # 점의 개수 = 가로 * 세로
    def num_points(self):
        raise NotImplementedError()

    # 변환된 바둑판
    def shape(self):
        raise NotImplementedError()

# 이름과 문자열을 이용하여 변환기 생성
def get_encoder_by_name(name, board_size):
    if isinstance(board_size, int):
        # board_size를 이용하여 정사각형 모양의 바둑판 생성
        board_size = (board_size, board_size)
    module = importlib.import_module(f'omok.encoders.{name}')
    # 변환기 구현시 인스턴스를 제공하는 create 함수 제공
    constructor = getattr(module, 'create')
    return constructor(board_size)