from argparse import Namespace
from typing import Any
import os

def run(args: Namespace, ctx: dict[str, Any]):
    if args.mode in {'config','all'}:
        os.system('projectsetup -R && projectsetup --update-all')
        os.system('docker system prune -f --volumes --all')
    if args.mode in {'data', 'all'}:
        restoremode = f'--zip {args.dbfile}' if args.local else '--s3'
        os.system(f'dbrestore --drop {restoremode}')
        os.system('dbrestore --post')