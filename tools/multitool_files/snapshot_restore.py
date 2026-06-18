import os
from argparse import Namespace
from typing import Any

def run(args: Namespace, ctx: dict[str, Any]):
    command = 'dbrestore --drop'
    if args.s3:
        command = ' '.join([command, '--s3'])
    elif args.filename:
        command = ' '.join([command, f'--zip {args.filename}'])
    else:
        command = ' '.join([command, '--zip backup.zip'])
    os.system(command)
    os.system('dbrestore --post')
