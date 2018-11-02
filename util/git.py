import os

from runner import Runner


class Git():
    def __init__(self, repository, workdir):
        self.repository = Runner.quote(repository)
        self.workdir = Runner.quote(workdir)

    def update(self):

        """更新仓库，如果工作目录不存在，则自动仓库并clone仓库"""

        cmd = []

        if not os.path.exists(self.workdir):
            cmd.append('mkdir -p ' + self.workdir)
            cmd.append('cd ' + self.workdir)
            # --quiet, -q
            cmd.append('git clone -q {} .'.format(self.repository))

        else:
            cmd.append('cd ' + self.workdir)
            # 更新仓库
            # --all Fetch all remotes
            # -p, --prune 将远程已经删除的分支从本地删除
            cmd.append('git fetch -q --all -p')
            # 重置工作区(未commit的数据全部还原)
            cmd.append('git reset -q --hard HEAD')
            # 清空未追踪的文件
            cmd.append('git clean -q  -d -f')

        return Runner([{'conn': 'local'}]).run('raw', ' && '.join(cmd))

    def chekcout(self, branch='master', commit='HEAD'):

        """切换到指定分支，并将代码重置为指定版本"""
        branch = Runner.quote(branch)
        commit = Runner.quote(commit)

        cmd = []
        cmd.append('cd ' + self.workdir)
        cmd.append('git checkout -q ' + branch)
        cmd.append('git reset -q --hard ' + commit)

        return Runner([{'conn': 'local'}]).run('raw', ' && '.join(cmd))


if __name__ == '__main__':
    git = Git('https://gitee.com/pfinal/test.git', '../temp')
    git.update()
    git.chekcout()
