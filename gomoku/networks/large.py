# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import Conv2D, ZeroPadding2D

# 오목 수 예측용 큰 합성곱 신경망 층 정의
def layers(input_shape):
    return [
        ZeroPadding2D((3, 3), input_shape=input_shape, data_format='channels_first'),
        Conv2D(64, (7, 7), padding='valid', data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(64, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(64, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(48, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(48, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(32, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D((2, 2), data_format='channels_first'),
        Conv2D(32, (5, 5), data_format='channels_first'),
        Activation('relu'),

        Flatten(),
        Dense(1024),
        Activation('relu'),
    ]