from argparse import Namespace
from typing import Any
import os


def run(args: Namespace, ctx: dict[str, Any]):
    command = 'runserver --shell=bash'
    os.system(command)