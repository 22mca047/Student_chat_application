from m1.v1.resource import *
from m1 import api

api.add_resource(CheckLogin, '/checklogin')
api.add_resource(Adddata, '/addData')
api.add_resource(Getall, '/getall')
api.add_resource(Fsdata, '/fsData')
api.add_resource(Bot, '/bot')

