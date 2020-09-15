# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from multiprocessing import Process, freeze_support
import os
import argparse

import h5py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint

from gomoku.agents.predict import DeepLearningAgent
from gomoku.data.processor import GomokuDataProcessor
from gomoku.encoders import get_encoder_by_name
from gomoku.networks import large

def main():
    """example :
    python generate_deep_learning_model.py --board-size 15 --encoder simple
    --num-games None --epochs 5 --batch-size 512 --model-out deep_bot.h5

    --num-games None : Use all data
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, required=True)
    parser.add_argument('--encoder', required=True)
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--epochs', '-e', type=int, default=5)
    parser.add_argument('--batch-size', '-b', type=int, default=512)
    parser.add_argument('--model-out', required=True)

    args = parser.parse_args()
    board_rows = board_cols = args.board_size
    num_classes = board_rows * board_cols
    num_games = args.num_games

    encoder = get_encoder_by_name(args.encoder, args.board_size)

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

    model_out = args.model_out

    # 체크포인트 저장 폴더 존재 여부 확인
    if not os.path.isdir('./checkpoints'):
        os.mkdir('./checkpoints')

    epochs = args.epochs
    batch_size = args.batch_size
    model.fit_generator(
        generator=generator.generate(batch_size, num_classes),
        epochs=epochs,
        steps_per_epoch=generator.get_num_samples() / batch_size,
        validation_steps=test_generator.get_num_samples() / batch_size,
        callbacks=[
            ModelCheckpoint('./checkpoints/' + model_out.replace('.h5', '') + '_{epoch}.h5')
        ]
    )
    model.evaluate_generator(
        generator=test_generator.generate(batch_size, num_classes),
        steps=test_generator.get_num_samples() / batch_size
    )

    # 모델 저장 폴더 존재 여부 확인
    if not os.path.isdir('./models'):
        os.mkdir('./models')

    output_file = './models/' + model_out

    deep_learning_bot = DeepLearningAgent(model, encoder)
    with h5py.File(output_file, 'w') as outf:
        deep_learning_bot.serialize(outf)

if __name__ == '__main__':
    main()