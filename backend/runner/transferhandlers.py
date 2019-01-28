#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen

from basehandler import BaseHandler

import pickle

MODEL_NUM = 0

class ImageHandler(BaseHandler):
    model = None
    num_models = 1

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        if self.model == None:
            yield self._load_model()
        image_info = self.request.files['image'][0]
        status = yield self._transform_with_model(image_info)
        print(status)
        self.write(status)

    @tornado.gen.coroutine
    def _transform_with_model(self, image):
        result = "/images/temp.png"
        # TODO: eval with model
        raise gen.Return(result)

    @tornado.gen.coroutine
    def _load_model(self):
        models = list(self.db.models.find({}).sort({'_id', -1}))
        self.num_models = len(models)
        print(models)
        model_str = models[MODEL_NUM % self.num_models]['model_str']
        self.model = pickle.loads(model_str)
        raise gen.Return(self.num_models)

class ModelHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        MODEL_NUM = self.get_int_arg('model_num', 0)
        self.write(str(MODEL_NUM))

