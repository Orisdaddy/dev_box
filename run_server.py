import subprocess
import sys

if __name__ == '__main__':
    subprocess.call(
        'gunicorn -c config/gunicorn djangoDT.wsgi:application',
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout
    )