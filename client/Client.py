import time
import nnpy
import json
import signal
import socket
import configparser
from docopt import docopt
from functools import partial
from multiprocessing import Process


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

    def start_module(self, process):
        pub = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        pub.connect('tcp://{}:{}'.format(self.server_ip, self.server_port))
        setattr(self, 'myprocess' , process)
        while True:
            message =  '{} {} {}'.format( self.timestamp(), self.nodeid, self.myprocess())
            pub.send(message)
            if self.debug:
                print(message)


def shutdown(signum, frame):
    print('Closing.')
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, partial(shutdown))

    client = Client()
    client.load_settings()

    for mod in client.modules.keys():
        # get the function from submodule
        m = __import__('{}.{}'.format('modules', mod ))
        l = getattr(m, mod)
        f = getattr(l, mod)

        Process(target=client.start_module, args=(f , )).start()
