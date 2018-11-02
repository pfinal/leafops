from flask import jsonify, request, g
from app.api import api
from app.model import to_dict

import json
import uuid

import os

from sqlalchemy import text

from app.model.base import db

from app.model.machine import Machine
from app.model.project import Project
from app.model.task import Task
from util.git import Git
from runner import Runner


@api.route('/task')
def task():
    models = Task.query.order_by('id desc').all()
    return jsonify({"status": True, 'data': [to_dict(m, append_columns=['project_name']) for m in models]})


@api.route('/task/create', methods=["POST"])
def task_create():
    model = Task()
    model.project_id = request.form['project_id']
    model.branch = request.form['branch']
    model.version = request.form['version']
    model.user_id = g.user_id

    db.session.add(model)
    db.session.commit()

    return jsonify({'status': True})


@api.route('/task/delete')
def task_delete():
    model = Task.query.get(request.args['id'])

    db.session.delete(model)
    db.session.commit()

    return jsonify({'status': True})


@api.route('/task/deploy', methods=["POST"])
def task_deploy():
    model = Task.query.get(request.form['id'])

    if deploy(model):
        task.status = 2
        db.session.commit()

        return jsonify({'status': True})
    return jsonify({'status': False})


def deploy(task):
    project = Project.query.get(task.project_id)
    print('[deploy: {}] '.format(project.name), end='')

    ids = json.loads(project.machine_ids)
    machine_all = Machine.query.filter(Machine.id.in_(ids)).all()

    workdir = "./runtime/{}/".format(project.id)

    file = pack(workdir, project.repository, task.branch, task.version)

    hosts = []
    for machine in machine_all:
        host = {'host': machine.ip, "user": machine.user, 'password': machine.password, 'name': machine.name}
        hosts.append(host)

    runner = Runner(hosts)

    # 部署代码
    code_dir = '/data/code/' + task.version
    deploy_dir = project.directory
    temp_file = '/tmp/' + str(uuid.uuid4().hex)
    runner.run('copy', {'src': file, 'dest': temp_file})

    # 创建源码目录和布署软连接的父目录
    # 例如 /data/webroot/myapp  创建并删除后，将留下 /data/webroot
    runner.run('raw', 'mkdir -p {0}; mkdir -p {1} && rm -rf {1}'.format(code_dir, deploy_dir))

    # 解压后删除压缩包
    runner.run('raw', 'mkdir -p {0} && cd {0} && tar -xzf {1} && rm -f {1}'.format(code_dir, temp_file))

    # 前置任务
    if project.pre_deploy:
        runner.run('raw', project.pre_deploy)

    # 更新软链接
    runner.run('raw', 'rm -f {0}; ln -s {1} {0}'.format(deploy_dir, code_dir))

    # 后置任务
    if project.post_release:
        runner.run('raw', project.post_release)

    os.remove(file)

    # git tag v2
    # git push origin master --tags

    print('success')

    return True


def pack(workdir, repository, branch, version):
    if not os.path.exists(workdir):
        os.mkdir(workdir)

    git = Git(repository, workdir + "git/")
    git.update()
    git.chekcout(branch, version)

    temp_file = str(uuid.uuid4().hex) + ".tar.gz"

    cmd = 'cd {} && tar -czf {} --exclude=.git .'.format(workdir + "git/", '../' + temp_file)

    Runner([{'conn': 'local'}]).run('raw', cmd)

    return workdir + temp_file
