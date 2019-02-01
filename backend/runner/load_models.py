from keras.models import load_model, Model
from keras.layers import Input

from transform import TransformNet

import keras_contrib
import os

MODELS_DIR = '/models/'

def load_model(n):
    models = [MODELS_DIR + m for m in os.listdir(MODELS_DIR)]
    m = models[n % len(models)]

    # load model with keras
    inputs = Input(shape=(720, 720, 3))
    transform_net = TransformNet(inputs, [32, 64, 128], 5)
    model = Model(inputs=inputs, outputs=transform_net)
    model.load_weights(m)
    
    return model

