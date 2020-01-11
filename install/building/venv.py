import subprocess


def pip_install(
        package, vision='',
        repository='-i https://pypi.tuna.tsinghua.edu.cn/simple',
        p=None,
        output=True
):
    if vision:
        vision = '==' + vision
    command = "pip3 install %s%s %s" % (package, vision, repository)
    if p:
        p.stdin.write(command.encode())
    else:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    if output:
        for line in iter(p.stdout.readline, b''):
            print(line.decode())
        p.stdout.close()
    p.wait()


def create_env(venv_name):
    pip_install('virtualenv')
    p = subprocess.Popen(f"virtualenv {venv_name}", shell=True)
    p.wait()

    # 下载python package
    p = subprocess.Popen(
        rf"cd {venv_name}/Scripts & activate & cd ../.. & pip3 install -r requirement/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple",
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    for line in iter(p.stdout.readline, b''):
        print(line.decode())
    p.stdout.close()
    p.wait()
