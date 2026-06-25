from ssh_client import SSHClient


class ToolRunner:

    def __init__(self, ssh):
        self.ssh = ssh

    def run(self, command):
        ok, output = self.ssh.run_command(command)
        return ok, output