import os
from argparse import Namespace
from typing import Any

BACKUP_DEFAULT = 'backup.zip'

def run(args: Namespace, ctx: dict[str, Any]):
    command = 'dbrestore --drop'
    if args.dl and args.s3:
        raise ValueError('dl and s3 are mutually exclusive')
    if args.dl:
        os.system(f'curl {args.dl} -o {args.filename}')
    if args.s3:
        command = ' '.join([command, '--s3'])
    else:
        command = ' '.join([command, f'--zip {args.filename}'])
    print(command)
    os.system(command)
    os.system('dbrestore --post')
