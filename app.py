# -*- coding: utf-8 -*-
from tornado.httpclient import AsyncHTTPClient
import tornado.ioloop
import sys
import logging
import os

from handlers.ConfigHandler import ConfigHandler
from handlers.RequestHandler import RequestHandler
from handlers.RegisterHandler import RegisterHandler

def __configure_logging():
    log_level = ConfigHandler.config["logging"]["level"]
    numeric_level = getattr(logging, log_level.upper(), None)
    log_config = ConfigHandler.config["logging"]
    log_file = log_config["filename"]
    logging.basicConfig(\
        level=numeric_level,\
        filename=log_file\
)


if __name__ == '__main__':

    __configure_logging()

    http_client = AsyncHTTPClient()
    request_handler = RequestHandler(http_client)
    register_handler = RegisterHandler(request_handler)

    register_handler.register_device() # efetivamente fazo registro aqui

    # SensorHandler pode ficar em segundo plano rodando lendo os sensores
    # e enviando requisições conforme a necessidade
    # sensor_handler = SensorHandler(request_handler)
    # sensor_handler.start_monitor()

    ioloop = tornado.ioloop.IOLoop.instance()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        print ('keyboard interrupt')
        sys.exit()