from pymongo import MongoClient

from keras.models import load_model

import keras_contrib
import os
import pickle

MODELS_DIR = '/models/'

client = MongoClient('mongodb://mongo:27017/')

models = [MODELS_DIR + m for m in os.listdir(MODELS_DIR)]

for m in models:
    # load model with keras
    model = load_model(m)

    # pickle to string
    serialized = pickle.dumps(model)

    # save to mongo
    client.models.insert_one({'model_str': serialized})

