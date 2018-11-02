import shutil
import subprocess


class Connection():

    def __init__(self, name='local'):
        self.name = name

    def start(self):
        pass

    def close(self):
        pass

    def run(cls, command):
        out_stream = subprocess.PIPE
        err_stream = subprocess.PIPE
        s = subprocess.Popen(command,
                             stderr=err_stream,
                             stdout=out_stream,
                             shell=True)
        (stdout, stderr) = s.communicate()

        return (
            s.returncode,
            stdout.decode('utf-8').strip() if stdout else '',
            stderr.decode('utf-8').strip() if stderr else '')

    def put(self, input, output):
        shutil.copyfile(input, output)

    def get(self, input, output):
        self.put(input, output)


if __name__ == '__main__':
    conn = Connection()
    conn.start()

    conn.put('./1.txt', './2.txt')
    conn.get('./2.txt', './3.txt')

    print(conn.run('uptime'))
