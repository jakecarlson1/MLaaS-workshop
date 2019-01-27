#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen

from basehandler import BaseHandler

import requests

class ImageHandler(BaseHandler):
    # TODO: timer to periodically update model
    runners = ['http://runner1:3000/', 'http://runner2:3000/']
    load_route = 'LoadModel/'
    transfer_route = 'Transfer/'
    curr_runner = 0
    curr_model = 0

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        image_info = self.request.files['image'][0]
        status = yield self._delegate_to_runner(image_info)
        print(status)
        self.write(status)

    @tornado.gen.coroutine
    def _delegate_to_runner(self, image):
        transfer_url = self.runners[self.curr_runner] + self.transfer_route
        # self.redirect(transfer_url)
        result = requests.post(transfer_url, files={'image': image['body']})
        raise gen.Return(result.text)

