# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import os

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint

from gomoku.data.processor import GomokuDataProcessor
from gomoku.encoders.oneplane import OnePlaneEncoder
from gomoku.networks import small

# 훈련/테스트 데이터
board_rows, board_cols = 15, 15
num_classes = board_rows * board_cols
num_games = None
# 바둑판 크기의 변환기 생성
encoder = OnePlaneEncoder((board_rows, board_cols))
# 바둑 데이터 처리기 초기화
processor = GomokuDataProcessor(encoder=encoder.name())
# 데이터 처리기를 이용하여 훈련데이터와 테스트데이터 제너레이터 생성
generator = processor.load_gomoku_data('train', num_games, use_generator=True)
test_generator = processor.load_gomoku_data('test', num_games, use_generator=True)

# small layer 모델 정의
input_shape = (encoder.num_planes, board_rows, board_cols)
network_layers = small.layers(input_shape)
model = Sequential()
for layer in network_layers:
    model.add(layer)
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# 모델 최적화 및 평가
epochs = 5
batch_size = 32

# 체크포인트 저장 폴더 존재 여부 확인
if not os.path.isdir('../checkpoints'):
    os.mkdir('../checkpoints')

model.fit_generator(
    generator=generator.generate(batch_size, num_classes),
    epochs=epochs,
    steps_per_epoch=generator.get_step(batch_size),
    validation_data=test_generator.generate(batch_size, num_classes),
    validation_steps=test_generator.get_step(batch_size),
    # 체크포인트 저장
    callbacks=[ModelCheckpoint('../checkpoints/small_model_epoch_{epoch}.h5')]

)
model.evaluate_generator(
    generator = test_generator.generate(batch_size, num_classes),
    steps=test_generator.get_num_samples() / batch_size
)

model.save('model_path.h5')