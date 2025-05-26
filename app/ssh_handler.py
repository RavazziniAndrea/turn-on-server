import paramiko

class SshHandler:
    ssh = paramiko.SSHClient()
    key_path = "/root/.ssh/id_ed25519"

    def _connect(ip_addr, username):
        key = paramiko.Ed25519Key(filename=SshHandler.key_path)
        SshHandler.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        SshHandler.ssh.connect(ip_addr, username=username , pkey=key)

    def run_ssh_cmd(ip_addr, username, cmd) -> str:
        SshHandler._connect(ip_addr, username)
        stdin, stdout, stderr = SshHandler.ssh.exec_command(cmd)
        s_stdout=stdout.read().decode()
        s_stderr=stderr.read().decode()
        SshHandler.ssh.close()
        return s_stdout, s_stderr
