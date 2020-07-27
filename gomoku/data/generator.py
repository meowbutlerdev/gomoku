# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import glob
import numpy as np
from keras.utils import to_categorical

class DataGenerator:
    def __init__(self, data_directory, samples):
        self.data_directory = data_directory
        self.samples = samples
        # 이전에 샘플링한 파일
        self.files = set(file_name for file_name, index in samples)
        self.num_samples = None

    # 샘플 수 확인
    def get_num_samples(self, batch_size=128, num_classes=15 * 15):
        if self.num_samples is not None:
            return self.num_samples
        else:
            self.num_samples = 0
            for X, y in self._generate(batch_size=batch_size, num_classes=num_classes):
                self.num_samples += X.shape[0]
            return self.num_samples

    # 오목 데이터의 다음 배치를 생성 후 반환
    def  _generate(self, batch_size, num_classes):
        for xml_file_name in self.files:
            file_name = xml_file_name.replace('.xml', '_') + 'train'
            feature_file = f'{self.data_directory}/{file_name}_features.npy'
            label_file = f'{self.data_directory}/{file_name}l_abels.npy'
            x = np.load(feature_file)
            y = np.load(label_file)
            x = x.astype('float32')
            y = to_categorical(y.astype(int), num_classes)
            while x.shape[0] >= batch_size:
                x_batch, x = x[:batch_size], x[batch_size:]
                y_batch, y = y[:batch_size], y[batch_size:]
                yield x_batch, y_batch

    # 모델 훈련에 생성기를 사용하기 위한 메서드
    def generate(self, batch_size=128, num_classes=15 * 15):
        while 1:
            for item in self._generate(batch_size, num_classes):
                yield item

