# pip3 install paramiko flask sqlalchemy flask_sqlalchemy -i https://pypi.tuna.tsinghua.edu.cn/simple
import random
import datetime

from flask import Flask as Flask, request, make_response, jsonify, g
from sqlalchemy import text

from app.model.base import db, Token

app = Flask(__name__)

# 加载配置文件
app.config.from_object('app.config')

# 注册蓝图
from app.api import api

app.register_blueprint(api)

db.init_app(app)


@app.before_request
def before_filter():
    # r = request
    # ip = request.remote_addr
    # url = request.url

    endpoint = request.endpoint
    print(endpoint)

    # auth_开头的接口不做验证
    if (endpoint is None or endpoint.startswith('api.auth_')) or endpoint in ['api.monitor_collect']:
        return

    t = request.args.get('token')
    if t is None:
        return jsonify({'status': False, 'data': 'INVALID_TOKEN'})

    one = Token.query.filter_by(token=t).first()
    if one == None:
        # return make_response('INVALID_TOKEN')
        return jsonify({'status': False, 'data': 'INVALID_TOKEN'})

    g.user_id = one.user_id

    # 清理过期的token 概率为0.1%
    if (random.randint(0, 1000000) < 1000000):
        dt = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        Token.query.filter(text('created_at < :created_at')).params({'created_at': dt}).delete(
            synchronize_session=False)
        db.session.commit()


@app.after_request
def after_filter(response):
    # print(response)

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT,'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    response.headers['Access-Control-Allow-Headers'] = allow_headers

    return response


if __name__ == '__main__':
    # 如果host缺省，只能本机访问
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
