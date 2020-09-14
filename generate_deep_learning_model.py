# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from multiprocessing import Process, freeze_support
import os

import h5py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint

from gomoku.agents.predict import DeepLearningAgent
from gomoku.data.processor import GomokuDataProcessor
from gomoku.encoders.simple import SimpleEncoder
from gomoku.networks import large

board_rows, board_cols = 15, 15
num_classes = board_rows * board_cols
num_games = None

encoder = SimpleEncoder((board_rows, board_cols))

processor = GomokuDataProcessor(encoder=encoder.name())

generator = processor.load_gomoku_data('train', num_games, use_generator=True)
test_generator = processor.load_gomoku_data('test', num_games, use_generator=True)

input_shape = (encoder.num_planes, board_rows, board_cols)
model = Sequential()
network_layers = large.layers(input_shape)
for layer in network_layers:
    model.add(layer)
model.add(Dense(num_classes, activation='softmax'))
model.compile(
    loss='categorical_crossentropy',
    optimizer='adadelta',
    metrics=['accuracy']
)

# 체크포인트 저장 폴더 존재 여부 확인
if not os.path.isdir('./checkpoints'):
    os.mkdir('./checkpoints')

epochs = 5
batch_size = 512
model.fit_generator(
    generator=generator.generate(batch_size, num_classes),
    epochs=epochs,
    steps_per_epoch=generator.get_num_samples() / batch_size,
    validation_steps=test_generator.get_num_samples() / batch_size,
    callbacks=[
        ModelCheckpoint('./checkpoints/deep_model_{epoch}.h5')
    ]
)
model.evaluate_generator(
    generator=test_generator.generate(batch_size, num_classes),
    steps=test_generator.get_num_samples() / batch_size
)

# 모델 저장 폴더 존재 여부 확인
if not os.path.isdir('./models'):
    os.mkdir('./models')

output_File = './models/deep_bot.h5'

deep_learning_bot = DeepLearningAgent(model, encoder)
with h5py.File(output_File, 'w') as outf:
    deep_learning_bot.serialize(outf)
