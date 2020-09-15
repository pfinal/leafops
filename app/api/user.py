import hashlib

from flask import jsonify, g

from app.model import to_dict
from app.model.base import db

from app.api import api
from app.model.user import User


@api.route('/user')
def user():
    users = User.query.order_by(User.id.desc()).all()

    return jsonify({'status': True, 'data': [to_dict(obj, ['id', 'username', 'created_at']) for obj in users]})
    # return dumps([to_dict(obj) for obj in users], ensure_ascii=False)


@api.route('/user/create', methods=["POST"])
def user_create():
    user = User('jack', '111111')
    password = '123456'
    user.password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()

    db.session.add(user)
    db.session.commit()

    return jsonify({'status': True})


@api.route('/user/delete')
def user_delete():
    return jsonify({'status': True})


@api.route('/user/update')
def user_update():
    one = User.query.filter_by(username='jack').first()
    one.status = 2
    db.session.add(one)
    db.session.commit()

    return jsonify({'status': True})


@api.route('/user/profile')
def user_profile():
    one = User.query.get(g.user_id)

    return jsonify({'status': True, 'data': to_dict(one, ['id', 'username', 'created_at'])})
