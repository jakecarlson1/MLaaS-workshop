#!/usr/bin/python
'''Starts and runs the tornado with BaseHandler '''

# tornado imports
import tornado.web
from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

# custom imports
from basehandler import BaseHandler
from transferhandlers import ImageHandler, ModelHandler

# Setup information for tornado class
define("port", default=3000,
       help="run on the given port", type=int)

# Utility to be used when creating the Tornado server
# Contains the handlers and the database connection
class Application(tornado.web.Application):
    def __init__(self):
        '''Store necessary handlers,
        connect to database
        '''

        handlers = [(r"/[/]?",             BaseHandler),
                    (r"/LoadModel[/]?",    ModelHandler),
                    (r"/Transfer[/]?",     ImageHandler),
                    ]

        settings = {'debug':True}
        tornado.web.Application.__init__(self, handlers, **settings)

    def __exit__(self):
        self.client.close()


def main():
    '''Create server, begin IOLoop
    '''
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()

