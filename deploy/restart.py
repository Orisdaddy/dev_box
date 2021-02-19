import sys
from paramiko import SSHClient, AutoAddPolicy

host = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
pro_path = sys.argv[4]

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(
    hostname=host,
    username=username,
    password=password
)

_, stdout, _ = ssh.exec_command(f'source {pro_path}/devbox1/bin/activate;cd {pro_path};'
                                f'python {pro_path}/devsm.py restart')
ssh.close()
