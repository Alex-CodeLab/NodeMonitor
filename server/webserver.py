# from flask import Flask, render_template, jsonify, make_response
#
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'some_secret_key.'
#
# @app.route('/')
# def index():
#     # socket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
#     context = { 'modules': server.modules, }
#     return render_template("main2.html", **context)
#
# @app.route('/data.json')
# def init_dashboard():
#     # send data currently in db
#     with open('db.pkl', 'rb') as f:
#         dq = pickle.load(f)
#     a = []
#     for mod in server.modules:
#         for message in dq[mod.encode('utf-8')] :
#             a.append(message.decode())
#
#     return jsonify({'msg': a, })
