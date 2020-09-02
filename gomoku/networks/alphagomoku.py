# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

from tensorflow.keras.model import Sequential
from tensorflow.keras.layers.core import Dense, Flatten
from tensorflow.keras.convolutional import Conv2D

# is_policy_net 변수를 통해 정책 신경망과 가치 신경망 선택
def alphagomoku_model(input_shape, is_policy_net=False, num_filters=192, \
                      first_kernel_size=5, other_kernel_size=3):
    model = Sequential()
    model.add(
        Conv2D(
            num_filters,
            first_kernel_size,
            input_shape=input_shape,
            padding='same',
            data_format='channels_first',
            activation='relu'
        )
    )

    for i in range(2, 12):
        model.add(
            Conv2D(
                num_filters,
                other_kernel_size,
                padding='same',
                data_format='channels_first',
                activation='relu'
            )
        )

    # 강한 정책 신경망
    if is_policy_net:
        model.add(
            Conv2D(
                filters=1,
                kernel_size=1,
                padding='same',
                data_format='channels_first',
                activation='relu'
            )
        )
        model.add(Flatten())
        return model
    # 가치 신경망
    else:
        model.add(
            Conv2D(
                num_filters,
                other_kernel_size,
                padding='same',
                data_format='channels_first',
                activation='relu'
            )
        )
        model.add(
            Conv2D(
                filters=1,
                kernel_size=1,
                padding='same',
                data_format='channels_first',
                activation='relu'
            )
        )
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(1, activation='tanh'))
        return model