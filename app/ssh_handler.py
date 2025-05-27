import paramiko
import socket

class SshHandler:
    ssh = paramiko.SSHClient()
    key_path = "/root/.ssh/id_ed25519"

    def is_server_on() -> bool:
        host = "10.0.42.250"
        port=22
        timeout=1
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, socket.error):
            return False

    def _connect(ip_addr, username):
        key = paramiko.Ed25519Key(filename=SshHandler.key_path)
        SshHandler.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        SshHandler.ssh.connect(ip_addr, username=username , pkey=key)

    def run_ssh_cmd(ip_addr, username, cmd) -> str:
        if not SshHandler.is_server_on():
            return "OFF", "OFF"
        SshHandler._connect(ip_addr, username)
        stdin, stdout, stderr = SshHandler.ssh.exec_command(cmd)
        s_stdout=stdout.read().decode()
        s_stderr=stderr.read().decode()
        SshHandler.ssh.close()
        return s_stdout, s_stderr
