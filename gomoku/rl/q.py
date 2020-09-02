# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import numpy as np
from tensorflow.keras.optimizers import SGD

from gomoku import encoders
from gomoku import board
from gomoku import kerasutil
from gomoku.agents.base import Agent

class QAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder
        self.collector = None
        self.temperature = 0.0

    # 정책의 임의성 정도 조절(ε)
    def set_temperature(self, temperature):
        self.temperature = temperature

    # 에이전트 경험 기록
    def set_collector(self, collector):
        self.collector = collector

    # 수 선택
    def select_move(self, game_state):
        board_tensor = self.encoder.encode(game_state)

        # 모든 가능한 수 리스트 생성
        moves = []
        board_tensors = []
        for move in game_state.legal_moves():
            if not move.is_play:
                continue
            moves.append(self.encoder.encode_point(move.point))
            board_tensors.append(board_tensor)

        num_moves = len(moves)
        board_tensors = np.array(board_tensors)
        # 모든 가능한 수에 대해 one_hot encoding
        move_vectors = np.zeros(
            (num_moves, self.encoder.num_points())
        )
        for i, move in enumerate(moves):
            move_vectors[i][move] = 1

        # 수 예측
        values = self.model.predict(
            [board_tensors, move_vectors]
        )
        # 가치값은 N * 1 행렬로, 이 때 N은 유효한 수의 갯수
        # reshape을 통해 N 크기의 벡터로 변경
        values = values.reshape(len(moves))

        # 수의 순위
        ranked_moves = self.rank_moves_eps_greedy(values)

        # 가장 앞의 유효한 수 선택
        for move_idx in ranked_moves:
            point = self.encoder.decode_point_index(moves[move_idx])
            # 경험 버퍼에 해당 결정 기록
            if self.collector is not None:
                self.collector.record_decision(
                    state=board_tensor,
                    action=moves[move_idx],
                )
            return board.Move.play(point)

    # 수 순위
    def rank_moves_eps_greedy(self, values):
        # 실제 수 대신 임의의 숫자로 순위 부여
        if np.random.random() < self.temperature:
            values = np.random.random(values.shape)
        # 작은 값부터 높은 값 순으로 수의 인덱스 정렬
        ranked_moves = np.argsort(values)
        return ranked_moves[::-1]

    # 경험 데이터로 훈련
    def train(self, experience, lr=0.1, batch_size=32):
        opt = SGD(lr=lr)
        self.model.compile(loss='mse', optimizer=opt)

        n = experience.states.shape[0]
        num_moves = self.encoder.num_points()
        y = np.zeros((n, ))
        actions = np.zeros((n, num_moves))
        for i in range(n):
            action = experience.actions[i]
            reward = experience.rewards[i]
            actions[i][action] = 1
            y[i] = reward

        self.model.fit(
            [experience.states, actions],
            y,
            batch_size=batch_size,
            epochs=1
        )