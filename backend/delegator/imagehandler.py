#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen

from basehandler import BaseHandler

import requests
import time

class ImageHandler(BaseHandler):
    # TODO: timer to periodically update model
    runners = ['http://runner1:3000/', 'http://runner2:3000/']
    load_route = 'LoadModel/'
    transfer_route = 'Transfer/'
    curr_runner = 0
    curr_model = 0
    last_update = time.time()
    model_update_interval = 20
    num_model = 3

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        if time.time() - last_update >= model_update_interval:
            status = yield self._update_model()
        image_info = self.request.files['image'][0]
        status = yield self._delegate_to_runner(image_info)
        print(status)
        self.write(status)

    @tornado.gen.coroutine
    def _delegate_to_runner(self, image):
        transfer_url = self.runners[self.curr_runner] + self.transfer_route
        result = requests.post(transfer_url, files={'image': image['body']})
        raise gen.Return(result.text)
    
    @tornado.gen.coroutine
    def _update_model(self):
        self.curr_model += 1
        self.curr_model %= self.num_models
        self.curr_runner += 1
        self.curr_runner %= len(self.runners)
        load_url = self.runners[self.curr_runner] + load_route
        result = requests.get(load_url, params={'model_num': self.curr_model})
        last_update = time.time()
        raise gen.Return(result.text)

