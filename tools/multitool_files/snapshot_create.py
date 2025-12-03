from argparse import Namespace
from typing import Any
import os


def run(args: Namespace, ctx: dict[str, Any]):
    command = f'dbbackup --filename {args.filename}'
    if not args.zip and not args.s3:
        args.zip = True
    if args.zip:
        command = ' '.join([command, '--format zip'])
    if args.s3:
        command = ' '.join([command, '--s3'])
    os.system(command)