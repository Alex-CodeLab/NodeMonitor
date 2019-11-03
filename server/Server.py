import zmq, nnpy
import configparser
import time
from db import Db
import struct, json, binascii, signal, pickle
from flask import Flask, render_template, jsonify, make_response
from multiprocessing import Process
from collections import deque
from functools import partial
from docopt import docopt
from pathlib import Path

class Server():
    """
    Usage:
    Server.py [-hvdw]

    Options:
    -d, --debug         Enable debugmessages
    -w, --no-webserver  Do not start webserver
    -h, --help          Show this help.
    -v, --version       Show version.
    """
    args = docopt(__doc__, version='0.1')

    def __init__(self):
        self.debug = self.args.get('--debug', False)
        config = configparser.ConfigParser()
        config.read('server.conf')
        self.modules = json.loads(config['DEFAULT'].get('modules','{}'))
        # self.dq = self.openDB()

    def __str__(self):
        return "Maven"

    def print(self, s):
        if self.debug:
            print(str(s))


    def maven(self, port, wsock_port ):

        sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        sub.bind('tcp://127.0.0.1:{}'.format(port))
        sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')

        # messaging to browser (webssocket)
        wsock = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        wsock.bind('ws://*:{}'.format(wsock_port))

        db = Db()
        i = 0
        while True:
            msg = sub.recv()
            wsock.send(msg)
            # add to db
            msgArray = msg.decode("utf-8").split(' ')
            module = msgArray[2]
            if module in self.modules.keys():
                db.write(msgArray[1], msg.decode("utf-8"), module)
            else:
                print('Unknown module {}. Ignored.'.format(module))


def shutdown(signum, frame):
    # todo: write to db
    print('Closing.')
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, partial(shutdown))

    server = Server()
    port = 5666
    websocket_port = 5555
    Process(target=server.maven, args=(port, websocket_port)).start()

    if not server.args.get('--no-webserver'):

        from webserver import *
        from flask import Flask, render_template, jsonify, make_response

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'some_secret_key.'
        db = Db()

        @app.route('/')
        def index():
            # socket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
            context = { 'modules': server.modules }
            return render_template("main2.html", **context)

        @app.route('/data/<module>')
        def get_data(module):
            print(module)
            db.read('machina', module)
            a = []

            return jsonify({'msg': a, })
        app.run(debug=False)
