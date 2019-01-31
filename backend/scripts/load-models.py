from pymongo import MongoClient

from keras.models import load_model, Model
from keras.layers import Input

from transform import TransformNet

import keras_contrib
import os
import pickle

MODELS_DIR = '/models/'

client = MongoClient('mongodb://mongo:27017/')

models = [MODELS_DIR + m for m in os.listdir(MODELS_DIR)]

for m in models:
    # load model with keras
    inputs = Input(shape=(720, 720, 3))
    transform_net = TransformNet(inputs, [32, 64, 128], 5)
    model = Model(inputs=inputs, outputs=transform_net)
    model.load_weights(m)

    # pickle to string
    serialized = pickle.dumps(model)

    # save to mongo
    client.models.insert_one({'model_str': serialized})

