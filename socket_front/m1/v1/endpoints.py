from m1.v1.resource import *
from m1 import api

api.add_resource(Login, '/')
api.add_resource(Register, '/register')
api.add_resource(Home, '/home')
api.add_resource(Chat, '/chat/<string:friend_id>')
api.add_resource(Bot, '/bot')