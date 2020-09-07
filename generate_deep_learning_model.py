# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import os

import h5py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from gomoku.agents.predict import DeepLearningAgent
from gomoku.data.processor import GomokuDataProcessor
from gomoku.encoders.simple import SimpleEncoder
from gomoku.networks import large

board_rows, board_cols = 15, 15
nb_classes = board_rows * board_cols
encoder = SimpleEncoder((board_rows, board_cols))
processor = GomokuDataProcessor(encoder=encoder.name())

X, y = processor.load_gomoku_data(num_samples=None)

input_shape = (encoder.num_planes, board_rows, board_cols)
model = Sequential()
network_layers = large.layers(input_shape)
for layer in network_layers:
    model.add(layer)
model.add(Dense(nb_classes, activation='softmax'))
model.compile(
    loss='categorical_crossentropy',
    optimizer='adadelta',
    metrics=['accuracy']
)

model.fit(X, y, batch_size=32, epochs=5, verbose=1)

# 모델 저장 폴더 존재 여부 확인
if not os.path.isdir('./models'):
    os.mkdir('./models')

output_File = './models/deep_bot.h5'

deep_learning_bot = DeepLearningAgent(model, encoder)
with h5py.File(output_File, 'w') as outf:
    deep_learning_bot.serialize(outf)