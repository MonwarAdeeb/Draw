import subprocess
import sys
import get_pip
import os
import importlib
import contextlib


def install(package):
    '''
    installs a package using pip

    :param package: string
    '''
    subprocess.call([sys.executable, "-m", "pip", "install", package])
