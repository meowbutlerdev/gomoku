# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import numpy as np
from keras import backend as K
from keras.optimizers import SGD

from gomoku.agent.base import Agent
from gomoku import encoders
from gomoku import board
from gomoku import kerasutil

# 확률분포 제한
def clip_probs(original_probs):
    min_p = 1e-5
    max_p = 1 - min_p
    clipped_probs = np.clip(original_probs, min_p, max_p)
    clipped_probs = clipped_probs / np.sum(clipped_probs)
    return clipped_probs

class PolicyAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder

    # ExperienceCollector아 PolicyAgent 결합
    def set_collector(self, collector):
        self.collector = collector

    # 신경망을 사용하여 수 선택
    def select_move(self, game_state):
        board_tensor = self.encoder.encode(game_state)
        # 케라스의 predict() 함수는 예측값을 배치로 만드므로
        # 단일 바둑판을 배열로 만든 후 첫 번째 결과 선택
        X = np.array([board_tensor])
        move_probs = self.model.predict(X)[0]

        move_probs = clip_probs(move_probs)

        # 바둑판의 모든 점의 인덱스를 갖는 배열 생성
        num_moves = self.encoder.board_width * self.encoder.board_height
        candidates = np.arange(num_moves)
        # 정책에 따라 바둑판의 점을 샘플링하여 시도할 점의 순서 리스트 생성
        ranked_moves = np.random.choice(
            candidates,
            num_moves,
            replace=False,
            p=move_probs
        )
        # 각 점을 반복하면서 유효한 수인지 확인 후 최초의 유효한 수를 선택
        for point_idx in ranked_moves:
            point = self.encoder.decode_point_index(point_idx)
            if game_state.is_valid_move(board.Move.play(point)):
                # 수를 선택하면 Collector에 전달
                if self.collector is not None:
                    self.collector.record_decision(
                        state=board_tensor,
                        action=point_idx
                    )
                return board.Move.play(point)

    # PolicyAgent 디스크에 기록
    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['board_width'] = self.encoder.board_width
        h5file['encoder'].attrs['board_height'] = self.encoder.board_height
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self._model, h5file['model'])

# 파일에서 정책 Agent 로드
def load_policy_agent(h5file):
    # 내장 케라스 함수를 이용하여 모델 구조와 가중치 로드
    model = kerasutil.load_model_from_hdf5_group(
        h5file['model'],
        custom_objects={'policy_gradient_loss': policy_gradient_loss}
    )
    # 변환기 복구
    encoder_name = h5file['encoder'].attrs['name']
    board_width = h5file['encoder'].attrs['board_width']
    board_height = h5file['encoder'].attrs['board_height']
    encoder = encoders.get_encoder_by_name(
        encoder_name,
        (board_width, board_height)
    )
    # Agent 재생성
    return PolicyAgent(model, encoder)