from .parser_generator import build_root_parser
import argparse
import argcomplete
from typing import Any
from .helper import SubcommandModule
from pathlib import Path
import importlib
import sys

def import_module(configroot: Path, path:str, module_name:str) -> SubcommandModule:
    file_path = str(configroot/path/f'{module_name}.py')
    # file_path = os.path.join(os.path.expanduser(path), f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_scripts(args: argparse.Namespace, target, scripts_mutable, root_parser, root_name, data):
    subparsers = data[target].get('subparsers')
    script = data[target].get('script')
    if script:
        scripts_mutable.append(script)
    if not subparsers:
        return
    if target != 'root':
        next_value = getattr(args, target)
    else:
        next_value = getattr(args, root_name)
    if subparsers and next_value is None:
        # if subcommands exist but no subcommand is used
        root_parser.parse_args(sys.argv[1:] + ['-h'])
        raise ValueError()
    if subparsers:
        get_scripts(args, next_value, scripts_mutable, root_parser, root_name, subparsers)

# 4. load and run scripts
def run(config_root, cfg):
    root_parser, root_name, data = build_root_parser(cfg)
    argcomplete.autocomplete(root_parser)
    scripts = []
    args, other_args = root_parser.parse_known_args()
    args.other_args = other_args
    get_scripts(args, 'root', scripts, root_parser, root_name, {'root': data})

    execution_context: dict[str, Any] = {}
    for script in scripts:
        mod = import_module(config_root, data['script_dir'], script)   
        mod.run(args, execution_context)

def run_from_manifest(config_root):
    from .build_config import read_manifest, build_config
    config_paths = read_manifest(config_root)
    cfg = build_config(config_root, config_paths)
    run(config_root, cfg)