import time
import os
import json
from jsonrpc_requests import Server, TransportError
import configparser

def btcnode(self):
    # listen to BTC node
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect ("tcp://%s:%s" %  (self.settings['btcnode'], self.settings['btcportzmq'],) )
    socket.setsockopt_string(zmq.SUBSCRIBE, "rawblock")
    pub = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
    pub.connect('tcp://127.0.0.1:5666')

    while True:
        msg = socket.recv_multipart()
        topic= msg[0]
        body = msg[1]
        if len(msg[-1]) == 4:
            msgSequence = struct.unpack('<I', msg[-1])[-1]
            sequence = str(msgSequence)
        if topic == b'rawblock':
            print('- RAW BLOCK HEADER ('+sequence+') -')
            # print(binascii.hexlify(body))
            # bc = get_blockcount()
            # pub.send(bc)


class Interval(object):
    def __init__(self, arg1):
        self.time = arg1

    def __call__(self, fn, *args, **kwargs):
        def new_func(*args, **kwargs):
            time.sleep(self.time)
            return fn(*args, **kwargs)
        return new_func


class Modules():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('client.conf')
        self.settings = config['node']

    def nodeconnect(self):
        # global node_proxy
        node_proxy = Server(
            "http://{}:{}@{}:{}".format(self.settings['rpcuser'], self.settings['rpcpassword'],
                                        self.settings['btcnode'], self.settings['rpcport']))
        return node_proxy


    ######
    @Interval(1)
    def load(self):
        avg_1, avg_5, avg_10 = list(map(str, os.popen('uptime')))[
            0].split(':')[-1].strip().split(', ')
        value = avg_1.replace(',', '.')
        return 'load ' + json.dumps({"value": value })

    @Interval(8)
    def mininginfo(self):
        node_proxy = self.nodeconnect()
        try:
            data = node_proxy.getmininginfo()
        except Exception as e:
            print(e)
            return
        data.pop('warnings')
        data.pop('pooledtx')
        r = json.dumps(data)

        return 'mininginfo ' + r

    @Interval(8)
    def chaintxstats(self):
        node_proxy = self.nodeconnect()
        try:
            data = node_proxy.getchaintxstats()
        except Exception as e:
            print(e)
            return
        data.pop('window_interval')
        data.pop('time')
        data.pop('window_final_block_hash')
        r = json.dumps(data)
        return 'chaintxstats ' + r

    @Interval(8)
    def mempoolinfo(self):
        node_proxy = self.nodeconnect()
        try:
            r = json.dumps(node_proxy.getmempoolinfo())
        except Exception as e :
            print(e)
            return

        return 'mempoolinfo ' + r
