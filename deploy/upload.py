import sys
import os
from paramiko import SFTPClient, Transport

root_path = os.path.dirname(__file__)

host = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
pro_path = sys.argv[4]

transport = Transport((host, 22))
transport.connect(
    username=username,
    password=password
)
sftp = SFTPClient.from_transport(transport)


def get_all_files(local_dir):
    all_files = list()
    for root, dirs, files in os.walk(local_dir, topdown=True):
        for file in files:
            filename = os.path.join(root, file)
            all_files.append(filename)
    return all_files


def mkdir(path_list, remote_dir):
    for i in path_list[2:]:
        path = os.path.join(remote_dir, i)
        try:
            sftp.stat(path)
        except FileNotFoundError:
            sftp.mkdir(path)


def sftp_put_dir(local_dir, remote_dir):
    if remote_dir[-1] == "/":
        remote_dir = remote_dir[0:-1]

    all_files = get_all_files(local_dir)
    with open(os.path.join(root_path, '.uploadignore')) as f:
        uploadignore = f.read().split('\n')
    for file in all_files:
        remote_filename = file.replace(local_dir, f'{remote_dir}/')
        remote_path = os.path.dirname(remote_filename)

        path_list = remote_path.split('/')
        jump_over = False
        for i in path_list[2:]:
            if i in uploadignore:
                jump_over = True
        if jump_over:
            break

        try:
            sftp.stat(remote_path)
        except FileNotFoundError:
            mkdir(path_list, remote_dir)
        print(f'{file} >>> Server')
        sftp.put(file, remote_filename)


if __name__ == '__main__':
    sftp_put_dir('./', pro_path)
    sftp.close()
