#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen

from basehandler import BaseHandler

import random
import requests
import uuid

SERVED_IMAGE_DIR = '/images/'

class ImageHandler(BaseHandler):
    # TODO: timer to periodically update model
    runners = ['http://runner1:3000/', 'http://runner2:3000/']
    load_route = 'LoadModel/'
    transfer_route = 'Transfer/'

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        curr_runner = yield self._update_model()
        image_info = self.request.files['image'][0]
        status = yield self._delegate_to_runner(image_info, curr_runner)
        print(status)
        self.write(status)

    @tornado.gen.coroutine
    def _delegate_to_runner(self, image, curr_runner):
        transfer_url = self.runners[curr_runner] + self.transfer_route
        result = requests.post(transfer_url, files={'image': image['body']})
        raise gen.Return(result.text)
    
    @tornado.gen.coroutine
    def _update_model(self):
        curr_model = random.randint(0, 100)
        curr_runner = random.randint(0, 100) % len(self.runners)
        load_url = self.runners[curr_runner] + self.load_route
        result = requests.get(load_url, params={'model_num': curr_model})
        raise gen.Return(curr_runner)

class ReturnHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        i_name = SERVED_IMAGE_DIR + 'temp.png'
        self.write_json({'image': i_name})

