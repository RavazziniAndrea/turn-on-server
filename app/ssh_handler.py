import paramiko
import socket

class SshHandler:
    ssh = paramiko.SSHClient()
    key_path = "/root/.ssh/id_ed25519"
    host = ""
    username = ""
    port=22
    timeout=1

    def is_server_on() -> bool:
        try:
            with socket.create_connection((SshHandler.host, SshHandler.port), timeout=SshHandler.timeout):
                return True
        except (socket.timeout, socket.error):
            return False

    def _connect():
        key = paramiko.Ed25519Key(filename=SshHandler.key_path)
        SshHandler.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        SshHandler.ssh.connect(SshHandler.host, username=SshHandler.username , pkey=key)

    def run_ssh_cmd(cmd) -> (str, str):
        if not SshHandler.is_server_on():
            return "OFF", "OFF"
        SshHandler._connect()
        stdin, stdout, stderr = SshHandler.ssh.exec_command(cmd)
        s_stdout=stdout.read().decode()
        s_stderr=stderr.read().decode()
        SshHandler.ssh.close()
        return s_stdout, s_stderr
