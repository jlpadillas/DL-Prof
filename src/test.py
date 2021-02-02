


import os

from subprocess import run       # para ejecutar un programa

def get_info():
    a = run(["cat", "/proc/cpuinfo"])
    print(a)

get_info()