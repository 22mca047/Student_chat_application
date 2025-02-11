from flask import Flask
from flask_restful import Api
import importlib

app = Flask(__name__)
api = Api(app)
app.secret_key = '123456'

importlib.import_module('m1.v1')