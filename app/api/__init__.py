from flask import Blueprint

api = Blueprint('api', __name__)

import app.api.user
import app.api.project
import app.api.machine
import app.api.task
import app.api.auth
import app.api.monitor
