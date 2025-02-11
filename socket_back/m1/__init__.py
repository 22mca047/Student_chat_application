# import eventlet
# eventlet.monkey_patch()

from flask import Flask, session
from flask_restful import Api
from sqlalchemy import create_engine
from flask_socketio import SocketIO
from flask_session import Session
from redis import StrictRedis
from flask_jwt_extended import JWTManager
import importlib
from flask_cors import CORS
from elasticsearch import Elasticsearch


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'h1i2t3e4s5h6'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.config['JWT_SECRET_KEY'] = 'h1i2t3e4s5h6123'
# app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")
CORS(app)
engine = create_engine('mysql+pymysql://root:root@localhost:3306/school_management')

redis = StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
es = Elasticsearch([{"host": "192.168.1.21", "port": 9200, "scheme": "http"}])
importlib.import_module('m1.v1')


