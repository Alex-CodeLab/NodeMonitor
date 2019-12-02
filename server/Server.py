import nnpy
import configparser
import time
from db import Store
import json
import binascii
import signal
from flask import Flask, render_template, jsonify, make_response
from multiprocessing import Process
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
        self.modules = json.loads(config['DEFAULT'].get('modules', '{}'))

    def __str__(self):
        return "Maven"

    def maven(self, port, wsock_port):
        # internal messaging
        sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        sub.bind('tcp://127.0.0.1:{}'.format(port))
        sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')

        # messaging to browser (webssocket)
        wsock = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        wsock.bind('ws://*:{}'.format(wsock_port))

        db = Store()
        i = 0
        self.init_batch()
        while True:
            msg = sub.recv()
            if self.debug:
                print(msg)
            wsock.send(msg)
            # add to db
            msgArray = msg.decode("utf-8").split(' ')
            client = msgArray[1]
            module = msgArray[2]
            if module in self.modules.keys():
                # add message to batch
                if client not in self.batch[module]:
                    self.batch[module] = {client: []}
                self.batch[module][client].append(msg.decode("utf-8"))
                i += 1
            else:
                print("Unknown module '{}'. Ignored.".format(module))
            if i >= 10:
                db.write(self.batch)
                self.init_batch()
                i = 0

    def init_batch(self):
        self.batch = {}
        for module in self.modules:
            self.batch[module] = {}


def shutdown(signum, frame):
    print('Closing.')
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, partial(shutdown))

    server = Server()
    port = 5666
    websocket_port = 5555
    Process(target=server.maven, args=(port, websocket_port)).start()

    if not server.args.get('--no-webserver'):

        from flask import Flask, render_template, jsonify, make_response

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'some_secret_key.'
        db = Store()


        @app.route('/')
        def react():
            context = {'modules': server.modules}
            return render_template("main2.html", **context)

        @app.route('/data/<module>')
        def get_data(module):
            data = db.read('machina', module)
            a = []
            return jsonify({'msg': data, })
        app.run(debug=False)
