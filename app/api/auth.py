import hashlib
import uuid

from flask import jsonify, request

from app.api import api
from app.model.base import db
from app.model.token import Token
from app.model.user import User


@api.route('/auth/token')
def auth_token():
    username = request.values.get('username')
    password = request.values.get('password')

    if not username or not password:
        return jsonify({'status': False, 'data': '用户名或密码无效'})

    hash = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()

    user = User.query.filter_by(username=username).first()
    if user == None or user.password != hash:
        return jsonify({'status': False, 'data': '用户名或密码无效'})

    token = Token()
    token.token = str(uuid.uuid4().hex)
    token.user_id = user.id
    db.session.add(token)
    db.session.commit()

    return jsonify({'status': True, 'data': {'token': token.token}})
