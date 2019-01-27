#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen

from basehandler import BaseHandler

class ImageHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        image_info = self.request.files['image'][0]
        status = yield self._transform_with_model(image_info)
        print(status)
        self.write(status)

    @tornado.gen.coroutine
    def _transform_with_model(self, image):
        result = "pass"
        # TODO: eval with model
        raise gen.Return(result)

class ModelHandler(BaseHandler):
    def post(self):
        # TODO: load newest model from mongo
        pass

