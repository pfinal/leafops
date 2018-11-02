import os
import uuid


class Action():

    def __init__(self, conn, module, param):
        '''
        :param conn: Connection
        :param module: raw ping script copy
        :param param: 根据module不同，param可能为string或dist
        '''
        self.conn = conn
        self.module = module
        self.param = param

    def execute(self):
        if self.module == 'raw':
            return self.conn.run(self.param)

        if self.module == 'ping':
            file = '{}/{}'.format(os.path.split(os.path.realpath(__file__))[0], self.module)
            return self.script(file)

        if self.module == 'script':
            return self.script(self.param)

        if self.module == 'copy':
            return self.conn.put(self.param['src'], self.param['dest'])

    def script(self, file):
        temp = '/tmp/{}'.format(uuid.uuid4().hex)
        self.conn.put(file, temp)

        result = self.conn.run('chmod +x {} && {}'.format(temp, temp))
        self.conn.run('rm -f '.format(temp))
        return result
