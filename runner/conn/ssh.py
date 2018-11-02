import os, paramiko


class Connection():

    def __init__(self, host, port=22, user='root', password=None, name=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.transport = paramiko.Transport((self.host, self.port))
        self.name = name if name is not None else host

    def start(self):

        if self.password:
            self.transport.connect(username=self.user, password=self.password)
        else:
            file = os.path.expanduser('~/.ssh/id_rsa')
            key = paramiko.RSAKey.from_private_key_file(file)
            self.transport.connect(username=self.user, pkey=key)

    def close(self):
        self.transport.close()

    def run(self, command):
        ssh = paramiko.SSHClient()

        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh._transport = self.transport
        stdin, stdout, stderr = ssh.exec_command(command)

        channel = stdout.channel
        status = channel.recv_exit_status()

        # code, stdout, err
        return (
            status,
            stdout.read().decode(),
            stderr.read().decode())

    def put(self, local, remote):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.put(local, remote)
        sftp.close()

    def get(self, remote, local):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.get(remote, local)
        sftp.close()


if __name__ == '__main__':
    conn = Connection('192.168.88.153', password='root')
    conn.start()

    conn.put('./1.txt', '/root/1.txt')
    conn.get('/root/1.txt', './2.txt')

    print(conn.run('uptime'))
