from runner.action import Action
import runner.conn.local
import runner.conn.ssh


class Runner():

    def __init__(self, hosts):
        self.hosts = hosts

    def run(self, module='ping', param=None):
        results = [self._run(host, module, param) for host in self.hosts]
        return results

    def _run(self, host, module, param):
        if 'conn' in host and host['conn'] == 'local':
            conn = runner.conn.local.Connection()
        else:
            conn = runner.conn.ssh.Connection(**host)

        conn.start()

        result = conn.name, Action(conn, module, param).execute()

        conn.close()

        return result

    @classmethod
    def quote(self, s):
        import re
        _find_unsafe = re.compile(r'[^\w@%+=:,./-]', re.ASCII).search

        """Return a shell-escaped version of the string *s*."""
        if not s:
            return "''"
        if _find_unsafe(s) is None:
            return s

        # use single quotes, and put single quotes into double quotes
        # the string $'b is then quoted as '$'"'"'b'
        return "'" + s.replace("'", "'\"'\"'") + "'"
