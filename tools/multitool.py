#!/usr/bin/python3
#PYTHON_ARGCOMPLETE_OK
from pathlib import Path
from multitool_lib import run_from_manifest

CONFIG_ROOT = Path(__file__).parent / 'multitool_files' /'yml'
run_from_manifest(CONFIG_ROOT)
