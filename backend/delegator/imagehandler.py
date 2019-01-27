#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen

from basehandler import BaseHandler

class ImageHandler(BaseHandler):
    # TODO: timer to periodically update model

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        image_info = self.request.files['image'][0]
        status = yield self._delegate_to_runner(image_info)
        print(status)
        self.write(status)

    @tornado.gen.coroutine
    def _delegate_to_runner(self, image):
        result = "pass"
        # TODO: send image to runner with newest model
        raise gen.Return(result)

