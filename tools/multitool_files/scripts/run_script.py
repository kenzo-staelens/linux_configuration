from argparse import Namespace
from typing import Any
import os


SHELL_MAPPING= {
    'sql': '--shell=sql',
    'shell': '--shell=bash',
    'odoo': '--shell=odoo',
    'debug': '--debugpy --debugpy-wait-for-attach',
    'dev': ''
}

def run(args: Namespace, ctx: dict[str, Any]):
    extra_args = args.other_args
    extra_args.append(f'--docker-odoo-port {args.port}')
    if args.run in SHELL_MAPPING:
        extra_args.append(SHELL_MAPPING.get(args.run))
    command = f'runserver {" ".join(extra_args)}'
    print(command)
    os.system(command)