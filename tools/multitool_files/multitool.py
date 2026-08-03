#!/usr/bin/python3
#PYTHON_ARGCOMPLETE_OK
from pathlib import Path
from sigil import run_from_config

CONFIG_ROOT = Path(__file__).parent
run_from_config(CONFIG_ROOT)
