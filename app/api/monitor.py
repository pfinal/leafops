import paramiko
from flask import jsonify, request

from app.api import api
from app.model.base import db
from app.model.machine import Machine
from app.model.monitor import Monitor


@api.route('/monitor/receive', methods=["POST"])
def monitor_receive():
    model = Monitor()

    ip = request.remote_addr

    machine = Machine.query.filter_by(ip=ip).first()
    if machine is None:
        return jsonify({'status': False, 'data': 'unknown ip'})

    model.machine_id = machine.id
    model.cpu = request.values.get('cpu')
    model.memory = request.values.get('memory')

    db.session.add(model)
    db.session.commit()

    return jsonify({'status': True, 'data': 'success'})


@api.route('/monitor/collect', methods=["GET"])
def monitor_collect():
    ssh = paramiko.SSHClient()

    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 如果已授权ssh免密码登录，则不需要传密码
    ssh.connect(hostname='192.168.88.88', username='root', password='root')
    # command = "free -m | awk '/^Mem/{print $7}'"  # 获取可用内存
    #uptime 
    command = "python3 /root/cpu.py"
    stdin, stdout, stderr = ssh.exec_command(command)

    channel = stdout.channel
    status = channel.recv_exit_status()

    return jsonify({
        'status': status == 0,
        'data': {'stdout': stdout.read().decode().strip(" \n"),
                 'stderr': stderr.read().decode().strip(" \n"), }
    })
