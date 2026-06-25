import paramiko
import os


class SSHClient:

    def __init__(self, host, username, key_path):
        self.host = host
        self.username = username
        self.key_path = key_path
        self.client = None

    def connect(self):

        if not os.path.exists(self.key_path):
            return False, "SSH Key not found."

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname=self.host,
                username=self.username,
                key_filename=self.key_path,
                timeout=10,
            )

            return True, "Connected"

        except Exception as e:
            return False, str(e)

    def disconnect(self):

        if self.client:
            self.client.close()

    def run_command(self, command):

        if self.client is None:
            return False, "Not Connected"

        try:

            stdin, stdout, stderr = self.client.exec_command(command)

            output = stdout.read().decode(errors="ignore")
            error = stderr.read().decode(errors="ignore")

            return True, output + error

        except Exception as e:
            return False, str(e)

    def check(self):

        if self.client is None:
            return False

        try:
            self.client.exec_command("echo test")
            return True
        except:
            return False