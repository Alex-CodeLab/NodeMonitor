#!/usr/bin/env python
import configparser
import json
import nnpy
import signal
import socket
import trio
import time
import os
import importlib

from docopt import docopt
from functools import partial

from modules import *

class Client():
    """
    Usage:
        Client.py [-hvd]

    Options:
        -d, --debug     Enable debugmessages
        -h, --help      Show this help.
        -v, --version   Show version.
    """
    args = docopt(__doc__, version='0.1')

    def __init__(self):
        self.debug = self.args.get('--debug', False)
        self.load_settings()

    def load_settings(self, configfile='client.conf'):
        config = configparser.ConfigParser()
        if not config.read(configfile):
            print("{} missing".format(configfile))
            exit()
        self.nodeid = config['DEFAULT'].get('id', socket.gethostname())
        self.server_ip = config['server'].get('ip', '127.0.0.1')
        self.server_port = config['server'].get('port', '5556')
        self.modules = json.loads(config['DEFAULT'].get('modules','{}'))
        return config

    def timestamp(self):
        return str(int(time.time()))

    def _debug(self, message):
        if self.debug:
            print(message)


    async def start_module(self, mod):
        pub = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        pub.connect('tcp://{}:{}'.format(self.server_ip, self.server_port))
        setattr(self, mod, eval(mod+'.'+mod))

        while True:
            c = getattr(self, mod)
            message = await c()
            message = json.loads(message)
            message['ts'] = self.timestamp()
            message['node'] = self.nodeid
            pub.send(json.dumps(message))
            self._debug(json.dumps(message))


if __name__ == '__main__':

    client = Client()

    async def parent():
        async with trio.open_nursery() as nursery:
            for mod in client.modules.keys():
                try:
                    nursery.start_soon(client.start_module, mod)
                finally:
                    print("Started: {}".format(mod))

            #clean shutdown
            with trio.open_signal_receiver(signal.SIGINT) as signal_aiter:
                async for signum in signal_aiter:
                    exit()

    trio.run(parent)
