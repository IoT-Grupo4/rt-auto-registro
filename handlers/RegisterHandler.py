# -*- coding: utf-8 -*-
from tornado.httpclient import HTTPResponse
from handlers.ConfigHandler import ConfigHandler
from tornado import gen
import time
import logging
import json

class RegisterHandler:

    @gen.coroutine
    def __check_register(self):
        token_file = self.register_info["token_file"]           
        try:
            with open(token_file,'r') as file:
                token_id = file.read()
                logging.debug('read token from file: '+token_id)

            if token_file != "" and token_file != None:
                logging.debug('valid token, returning')
                return True

        except FileNotFoundError:
            logging.debug('token not found, registering...')
            return False

    def __init__(self, request_handler):

        self.register_info = ConfigHandler.config["register_info"]
        self.request_handler = request_handler

    @gen.coroutine
    def register_device(self):

        """ Conforme especificação da APi em:
            http://docs.uiot.org/raise/#/
            Exemplo: 
            {
                "name": "Raspberry PI",     
                "chipset": "AMD 790FX",
                "mac": "FF:FF:FF:FF:FF:FF",
                "serial": "C210",
                "processor": "Intel I3",
                "channel": "Ethernet",
                "timestamp": 1317427200
            }
        """
        is_registered = yield self.__check_register()
        if not is_registered: # verifica se precisa registrar!
            
            post_data = {
                "name": self.register_info["name"],
                "chipset": self.register_info["chipset"],
                "mac": self.register_info["mac"],
                "serial": self.register_info["serial"],
                "processor": self.register_info["processor"],
                "channel": self.register_info["channel"],
                "timestamp": int(time.time())
            }

            url = self.register_info["raise_url"]+\
                self.register_info["client_register_path"]

            http_response = yield self.request_handler.send_data(url, post_data)
            logging.debug('http_response')

            logging.debug(http_response)
            if http_response:
                http_response = json.loads(http_response.body.decode('utf-8'))
                token_id = http_response["tokenId"]
                logging.debug('Register request completed')
                logging.debug('received token: '+token_id)

                # Salva o arquivo de token
                if http_response["code"] == "200":
                    token_file = self.register_info["token_file"]           
                    with open(token_file,'w') as file:
                        file.write(token_id)
                        logging.debug('token written to file '+token_file)
                else:
                    logging.debug('response_code !=- 200')

            else:
                logging.debug('Failed to complete request')

