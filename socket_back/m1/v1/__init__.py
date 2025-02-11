from flask import Blueprint
from m1 import app, api, socketio
from m1.v1 import resource

blueprint = Blueprint('m1', __name__)
api.blueprint_setup = blueprint
api.blueprint = blueprint

from m1.v1 import endpoints

app.register_blueprint(blueprint)
socketio.on_namespace(resource.Chat('/chat'))

