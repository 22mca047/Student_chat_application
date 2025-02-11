from flask import Blueprint
from m1 import app, api

blu = Blueprint('blueprint', __name__)
api.blueprint_setup = blu
api.blueprint = blu

from m1.v1 import endpoints

app.register_blueprint(blu)