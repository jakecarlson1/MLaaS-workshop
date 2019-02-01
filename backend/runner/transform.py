from keras.layers import (Conv2D, Conv2DTranspose, Input,
        Lambda, Activation, Cropping2D, ZeroPadding2D)
from keras.models import Model
import keras.layers
from keras.initializers import TruncatedNormal
import tensorflow as tf

from keras_contrib.layers.normalization import InstanceNormalization

WEIGHTS_INIT_STDEV = .1

class ReflectionPadding2D(ZeroPadding2D):
    def call(self, x, mask=None):
        (top_pad, bottom_pad), (left_pad, right_pad) = self.padding
        paddings = [[0, 0],
                    [top_pad, bottom_pad],
                    [left_pad, right_pad],
                    [0, 0]]
        return tf.pad(x, paddings, mode='REFLECT')

def Conv2DInstanceNorm(inputs, filters, kernel_size,
                           strides=1, relu=True):
    weights_init = TruncatedNormal(stddev=WEIGHTS_INIT_STDEV, seed=1)
    conv = Conv2D(filters,
                  (kernel_size, kernel_size),
                  strides=strides,
                  padding='same',
                  kernel_initializer=weights_init,
                  use_bias=False)(inputs)
    norm = InstanceNormalization(axis=3)(conv)
    if relu:
        norm = Activation('relu')(norm)
    return norm

def Conv2DTransposeInstanceNorm(inputs, filters, kernel_size,
                                strides=1, relu=True):
    weights_init = TruncatedNormal(stddev=WEIGHTS_INIT_STDEV, seed=1)
    conv = Conv2DTranspose(filters,
                           (kernel_size, kernel_size),
                           strides=strides,
                           padding='same',
                           kernel_initializer=weights_init,
                           use_bias=False)(inputs)
    norm = InstanceNormalization(axis=3)(conv)
    if relu:
        norm = Activation('relu')(norm)
    return norm

def Conv2DResidualBlock(inputs, filters):
    tmp     = Conv2DInstanceNorm(inputs, filters, 3)
    tmp2    = Conv2DInstanceNorm(tmp, filters, 3, relu=False)
    return keras.layers.add([inputs, tmp2])

def TransformNet(inputs, conv_filters, num_resids):
    net = ReflectionPadding2D(30)(inputs)
    net = Conv2DInstanceNorm(net, conv_filters[0], 9)
    for filters in conv_filters[1:]:
        net = Conv2DInstanceNorm(net, filters, 3, strides=2)
    for i in range(num_resids):
        net = Conv2DResidualBlock(net, conv_filters[-1])
    for filters in conv_filters[::-1][1:]:
        net = Conv2DTransposeInstanceNorm(net, filters, 3, strides=2)
    net = Conv2DInstanceNorm(net, 3, 9, relu=False)
    net = Activation('tanh')(net)
    net = Cropping2D(30)(net)
    preds = Lambda(lambda x : x * 150 + 255./2)(net)
    return preds
