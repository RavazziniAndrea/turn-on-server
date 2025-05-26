import paramiko

class SshHandler:
    ssh = paramiko.SSHClient()

    def _connect(ip_addr):
        SshHandler.ssh.connect(ip_addr, username="", password="")

    def run_ssh_cmd(ip_addr, username, password, cmd) -> str:
        SshHandler._connect(ip_addr)
        stdin, stdout, stderr = SshHandler.ssh.exec_command(cmd)
        SshHandler.ssh.close()
        return stdout, stderr
