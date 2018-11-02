from flask import Flask as Flask
from sqlalchemy import text

from app.model.base import db
import time

from app.model.task import Task

from app.api.task import deploy

app = Flask(__name__)

app.config.from_object('app.config')

db.init_app(app)


def handler():
    task = Task.query.filter(text('status=:status')).params(status=1).first()

    if task is None:
        return 0

    if deploy(task):
        task.status = 2
        db.session.commit()


while True:

    with app.app_context():
        if handler() == 0:
            time.sleep(1)
