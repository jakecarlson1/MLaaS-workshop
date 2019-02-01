#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen

from scipy.misc import imsave

from PIL import Image

from basehandler import BaseHandler

from load_models import load_model

import uuid

import numpy as np

MODEL_NUM = 0

class ImageHandler(BaseHandler):
    model = None

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        if self.model == None:
            yield self._load_model()
        image_info = self.request.files['image'][0]
        status = yield self._transform_with_model(image_info['body'])
        print(status)
        self.write(status)

    @tornado.gen.coroutine
    def _transform_with_model(self, image_body):
        # image = np.fromstring(image_body, dtype=np.uint8)
        # image = image.reshape(720,720,4)
        image = Image.frombytes('RGB', (720,720), image_body)
        data = image.getdata()
        print(len(list(data)))
        pred = self.model.predict([image])[0]
        image_path = "/images/" + str(uuid.uuid4()) + ".jpeg"
        imsave(image_path, pred)
        raise gen.Return(image_path)

    @tornado.gen.coroutine
    def _load_model(self):
        self.model = load_model(MODEL_NUM)
        raise gen.Return()

class ModelHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        MODEL_NUM = self.get_int_arg('model_num', 0)
        self.write(str(MODEL_NUM))

