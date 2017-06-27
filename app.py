#!/usr/bin/env python

import uuid
import logging
import redis
from tornado.web import URLSpec
from tornado.options import options
import tornado.websocket
import tornadobase.application
import tornadobase.handlers


redisConn = redis.StrictRedis(host='localhost',
                              port=6379,
                              db=0,
                              decode_responses=True)


class IndexHandler(tornadobase.handlers.BaseHandler):

    def get(self):
        self.render('index.tmpl.html')


class PeerSignalingHandler(tornado.websocket.WebSocketHandler):

    clients = {}

    def open(self):
        '''
        Add record of client to redis by uuid
        '''
        self.clientid = uuid.uuid4().hex
        redisConn.set(self.clientid, 'connected')
        self.clients[self.clientid] = {}

        self.write_message({
            'type': 'connected',
            'clientid': self.clientid})

    def on_message(self, message):
        logging.info(message)

    def on_close(self):
        '''
        Remove client record from redis
        '''
        logging.info('client disconnected')
        redisConn.delete(self.clientid)
        self.clients.pop(self.clientid, None)


class Application(tornadobase.application.Application):

    def init_handlers(self):

        self.handlers = [
            URLSpec(r'/', IndexHandler, name='Home'),
            URLSpec(r'/peers', PeerSignalingHandler, name='PeerSocket')
        ]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    options.parse_command_line()
    app = Application()
    app.start()
