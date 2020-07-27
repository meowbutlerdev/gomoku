# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import os.path
import glob
from xml.etree.ElementTree import parse

import numpy as np
from keras.utils import to_categorical

from gomoku.notation import Gomoku_game
from gomoku.board import GameState, Move
from gomoku.types import Point
from gomoku.encoders.base import get_encoder_by_name
from gomoku.data.index_processor import Index
from gomoku.data.sampling import Sampler

# 변환기와 디렉토리를 지정하여 데이터 전처리기 초기화
class GomokuDataProcessor:
    def __init__(self, encoder='oneplane', data_directory='data'):
        self.encoder = get_encoder_by_name(encoder, 15)
        self.data_dir = data_directory

    # 데이터를 로드하여 전처리 후 저장
    # data_type에 train/test를 지정
    # num_samples에 데이터 수를 지정
    def load_gomoku_data(self, data_type='train', num_samples=1000):
        index = Index(data_directory=self.data_dir)
        index.download_files()

        sampler = Sampler(data_dir=self.data_dir)
        data = sampler.draw_data(data_type, num_samples)
        xml_names = set()
        for filename in data:
            # 기보 파일명 저장
            xml_names.add(filename)

        for xml_name in xml_names:
            base_name = xml_name.replace('.xml', '')
            data_file_name = base_name + '_' + data_type
            if not os.path.isfile(self.data_dir + '/' + data_file_name):
                self.process_xml(xml_name, data_file_name)

        # 각 기보의 feature와 label 반환
        features_and_labels = self.consolidate_games(data_type, data)
        return features_and_labels

    # xml 형식으로 저장된 기보 파일을 feature와 label로 변환
    def process_xml(self, xml_file_name, data_file_name):
        notation_content = self.total_moves(xml_file_name)

        gomoku_game = Gomoku_game()
        notation = gomoku_game.from_string(notation_content)

        if notation == None:
            return None

        # 배열 크기 확인
        total_examples = len(notation)
        shape = self.encoder.shape()
        feature_shape = np.insert(shape, 0, total_examples)
        features = np.zeros(feature_shape)
        labels = np.zeros((total_examples, ))

        game_state = GameState.new_game(15)

        counter = 0
        for color, move_tuple in notation:
            row, col = move_tuple
            point = Point(row, col)
            move = Move.play(point)
            features[counter] = self.encoder.encode(game_state)
            labels[counter] = self.encoder.encode_point(point)
            counter += 1

            game_state = game_state.apply_move(move)

        feature_file_base = self.data_dir + '/' + data_file_name + '_features'
        label_file_base = self.data_dir + '/' + data_file_name + '_labels'

        np.save(feature_file_base, features)
        np.save(label_file_base, labels)

    # feature와 label을 묶음
    def consolidate_games(self, data_type, samples):
        files_needed = set(file_name for file_name in samples)
        file_names = []
        for xml_file_name in files_needed:
            file_name = xml_file_name.replace('.xml', '_') + data_type
            file_names.append(file_name)

        feature_list = []
        label_list = []
        for file_name in file_names:
            try:
                feature_file = f'{self.data_dir}/{file_name}_features.npy'
                label_file = f'{self.data_dir}/{file_name}l_abels.npy'
                x = np.load(feature_file)
                y = np.load(label_file)
                x = x.astype('float32')
                y = to_categorical(y.astype(int), 15 * 15)
                feature_list.append(x)
                label_list.append(y)
            except FileNotFoundError:
                print(f'{self.data_dir}/{file_name}_*_.npy is not found.')

        features = np.concatenate(feature_list, axis=0)
        labels = np.concatenate(label_list, axis=0)
        np.save(f'{self.data_dir}/features_{data_type}.npy', features)
        np.save(f'{self.data_dir}/labels_{data_type}.npy', labels)

        return features, labels

    def total_moves(self, xml_file_name):
        game_list = parse(self.data_dir + '/' + xml_file_name)
        board = game_list.find('board')
        notation_content = board.text.split(' ')
        return notation_content