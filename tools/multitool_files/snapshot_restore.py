import os
from argparse import Namespace
from typing import Any

def run(args: Namespace, ctx: dict[str, Any]):
    command = 'dbrestore --drop'
    if args.filename:
        command = ' '.join([command, f'--zip {args.filename}'])
    else:
        command = ' '.join([command, '--s3'])
    os.system(command)
    os.system('dbrestore --post')