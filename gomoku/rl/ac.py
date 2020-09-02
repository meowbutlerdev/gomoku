# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import numpy as np
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import SGD

from gomoku.agents.base import Agent
from gomoku import encoders
from gomoku import board
from gomoku import kerasutil

class ACAgent(Agent):
    def __init__(self, model, encoder):
        # 케라스 순차모델 인스턴스
        self.model = model
        # Encoder 인터페이스
        self.encoder = encoder
        self.collector = None

    # ExperienceCollector와 PolicyAgent 결합
    def set_collector(self, collector):
        self.collector = collector

    # 신경망을 사용하여 수 선택
    def select_move(self, game_state):
        board_tensor = self.encoder.encode(game_state)
        # 케라스의 predict() 함수는 예측값을 배치로 만드므로
        # 단일 바둑판을 배열로 만든 후 첫 번째 결과 선택
        X = np.array([board_tensor])

        # 출력값이 두 개이므로 넘파이 배열로 이루어진 튜플을 반환
        actions, values = self.model.predict(X)
        # 수 분포가 필요한 배열의 첫 번째 원소 선택
        move_probs = actions[0]
        # 가치는 1차원 벡터이므로 벡터의 첫 번째 원소 선택
        estimated_value = values[0][0]

        eps = 1e-6
        move_probs = np.clip(move_probs, eps, 1 - eps)
        move_probs = move_probs / np.sum(move_probs)

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
                    # 경험 버퍼의 추정치 포함
                    self.collector.record_decision(
                        state=board_tensor,
                        action=point_idx,
                        estimated_value=estimated_value
                    )
                return board.Move.play(point)

    # PolicyAgent를 디스크에 기록
    def serialize(self, h5file):
        """To use this method,
        first create a new HDF5 file and then process it for it.

        example :
        import h5py
        with h5py.File(output_file, 'w') as outf:
            agents.serialize(outf)
        """
        h5file.create_group('encoder')
        # 바둑판 변환기 재생성에 필요한 정보 저장
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['board_width'] = self.encoder.board_width
        h5file['encoder'].attrs['board_height'] = self.encoder.board_height
        h5file.create_group('model')
        # 모델과 가중치 저장
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])

    # 정책 경사 학습을 사용하여 경험 데이터로 에이전트 훈련
    def train(self, experience, lr=0.1, batch_size=32):
        opt = SGD(lr=lr)
        self.model.compile(
            optimizer=opt,
            loss=['categorical_crossentropy', 'mse'],
            # 1.0은 정책 출력, 0.5는 가치 출력에 적용
            loss_weights=[1.0, 0.5]
        )

        n = experience.states.shape[0]
        num_moves = self.encoder.num_points()
        policy_target = np.zeros((n, num_moves))
        value_target = np.zeros((n, ))
        for i in range(n):
            # 어드밴티지에 따라 가중치 부여
            action = experience.actions[i]
            policy_target[i][action] = experience.advantages[i]
            reward = experience.rewards[i]
            value_target[i] = reward

        self.model.fit(
            experience.states,
            [policy_target, value_target],
            batch_size=batch_size,
            epochs=1
        )

def load_ac_agent(h5file):
    # 모델 구조와 가중치 로드
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    # 변환기 복구
    encoder_name = h5file['encoder'].attrs['name']
    if not isinstance(encoder_name, str):
        encoder_name = encoder_name.decode('ascii')
    board_width = h5file['encoder'].attrs['board_width']
    board_height = h5file['encoder'].attrs['board_height']
    encoder = encoders.get_encoder_by_name(
        encoder_name,
        (board_width, board_height)
    )
    # Agent 재생성
    return ACAgent(model, encoder)