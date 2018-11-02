from flask import jsonify, request
from app.api import api
from app.model import to_dict
from app.model.base import db
from app.model.machine import Machine
from runner import Runner


@api.route('/machine')
def machine():
    query = Machine.query.order_by('id desc')

    print(request.args.get('name'))

    if request.args.get('name') != None and request.args.get('name') != '':
        query = query.filter('name like :name').params(name=request.args.get('name') + "%")

    models = query.all()

    return jsonify({"status": True, "data": [to_dict(m, append_columns=['cpu', 'mem']) for m in models]})


@api.route('/machine/create', methods=['POST'])
def machine_create():
    model = Machine()
    model.name = request.form['name']
    model.ip = request.form['ip']
    model.user = request.form['user']
    model.password = request.form['password']

    db.session.add(model)
    db.session.commit()

    return jsonify({'status': True})


@api.route('/machine/delete')
def machine_delete():
    model = Machine.query.get(request.args['id'])

    db.session.delete(model)
    db.session.commit()

    return jsonify({'status': True})


@api.route('/machine/update', methods=['POST'])
def machine_update():
    model = Machine.query.get(request.form['id'])

    model.name = request.form['name']
    model.ip = request.form['ip']
    model.user = request.form['user']
    model.password = request.form['password']

    db.session.commit()

    return jsonify({'status': True, 'data': ''})


@api.route('/machine/test')
def machine_test():
    '''测试指定主机是否能连接'''
    model = Machine.query.get(request.args.get('id'))

    try:

        host = {'host': model.ip, "user": model.user, 'password': model.password, 'name': model.name}

        runner = Runner([host])

        results = runner.run('raw', "lscpu | awk '/^CPU\(s\)/{print $2}'")
        code, cpu, err = results[0][1]
        if code != 0:
            return jsonify({'status': False, "data": err})

        results = runner.run('raw', "free | awk '/^Mem/{print $2}'")
        code, mem, err = results[0][1]
        if code != 0:
            return jsonify({'status': False, "data": err})

        hardware = {'cpu': str(cpu).strip(), 'mem': str(mem).strip()}

        import json

        if model.hardware != '':
            temp = json.loads(model.hardware)
            temp['cpu'] = hardware['cpu']
            temp['mem'] = hardware['mem']
        else:
            temp = hardware

        model.hardware = json.dumps(temp)

        db.session.commit()

        return jsonify({'status': True, "data": hardware})


    except Exception as ex:
        print(ex)
        return jsonify({'status': False, "data": str(ex)})
