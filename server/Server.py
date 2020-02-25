import nnpy
import configparser
import time
import json
from db import Store
import json, binascii, signal
from flask import Flask, render_template, jsonify, make_response
from multiprocessing import Process
from functools import partial
from docopt import docopt
# from pathlib import Path

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

    def _debug(self, message):
        if self.debug:
            print(message)

    def maven(self, port, wsock_port):
        """
        Collects all messages by listening for any incoming data from clients
        and stores it to a internal rrdb
        """

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
            self._debug(msg)
            wsock.send(msg)
            msgJson = json.loads(msg.decode("utf-8"))

            client = msgJson['node']
            module = msgJson['module']
            if module in self.modules.keys():
                # add message to batch
                if client not in self.batch[module]:
                    self.batch[module] = {client: []}
                self.batch[module][client].append(msg.decode("utf-8"))
                i += 1
            else:
                print("Unknown module '{}'. Ignored.".format(module))
            if i >= 10:
                # add to db
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
        from flask_cors import CORS, cross_origin

        # flask
        app = Flask(__name__,
                static_url_path='',
                static_folder='frontend/dist',
                template_folder='frontend/dist')

        cors = CORS(app)
        app.config['SECRET_KEY'] = 'some_secret_key.'
        app.config['CORS_HEADERS'] = 'Content-Type'

        db = Store()

        # flask routes
        @app.route('/')
        def react():
            context = {'modules': server.modules}
            return render_template("index.html", **context)


        @app.route('/data/<module>')
        @cross_origin()
        def get_data(module):
            data = db.read('machina', module)

            return jsonify({'msg': data, })
        app.run(debug=True)
