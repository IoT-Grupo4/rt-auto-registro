# -*- coding: utf-8 -*-
from tornado.httpclient import HTTPResponse,\
                                HTTPRequest, HTTPError
from tornado import gen
import json
import time
import logging

from handlers.ConfigHandler import ConfigHandler

class RequestHandler:

    def __init__(self, http_client):
        self.http_client = http_client
        self.http_header = {"Content-Type": "application/json; charset=UTF-8"}

    @gen.coroutine
    def send_data(self, url, data):

        http_req = HTTPRequest(\
            url=url,\
            method='POST',\
            body=json.dumps(data),\
            headers=self.http_header\
        )

        try:
            logging.debug('url: '+url)
            logging.debug('Trying to do http request with data:')
            logging.debug(data)
            http_response = yield self.http_client.fetch(http_req)

            logging.debug('Response: ')
            logging.debug(http_response.body)

            if http_response.error:
                logging.debug("Error: ",http_response.error)

        except:
            http_response = False

        print(http_response)
        return http_response
