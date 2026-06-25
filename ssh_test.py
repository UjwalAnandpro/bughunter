from ssh_client import SSHClient

ssh = SSHClient(
    host="192.168.137.190",
    username="ujwal",
    key_path=r"C:\Users\ujwal\.ssh\id_ed25519"
)

ok, msg = ssh.connect()

print(ok)
print(msg)

if ok:

    ok, output = ssh.run_command("whoami")

    print(output)

    ssh.disconnect()