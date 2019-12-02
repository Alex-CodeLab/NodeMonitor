import configparser
import json
import nnpy
import signal
import socket
import trio
import time
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

    def load_settings(self):
        config = configparser.ConfigParser()
        config.read('client.conf')
        self.nodeid = config['DEFAULT'].get('id', socket.gethostname())
        self.server_ip = config['server'].get('ip', '127.0.0.1')
        self.server_port = config['server'].get('port', '5556')
        self.modules = json.loads(config['DEFAULT'].get('modules','{}'))

    def timestamp(self):
        return str(int(time.time()))


    async def start_module(self, mod):
        pub = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        pub.connect('tcp://{}:{}'.format(self.server_ip, self.server_port))
        setattr(self, mod, eval(mod+'.'+mod))

        while True:
            c = getattr(self, mod)
            r = await c()
            message =  '{} {} {}'.format( self.timestamp(), self.nodeid, r)
            pub.send(message)
            if self.debug:
                print(message)




client = Client()
client.load_settings()
async def parent():
    async with trio.open_nursery() as nursery:
        for mod in [ 'load', 'memory']:
            # m = __import__('{}.{}'.format('modules', mod ))

            # load = importlib.import_module('{}.{}'.format('modules', mod ))
            nursery.start_soon(client.start_module, mod)

trio.run(parent)
