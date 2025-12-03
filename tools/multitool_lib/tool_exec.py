from .parser_generator import build_root_parser
import argparse
import argcomplete
from typing import Any, cast
from .helper import SubcommandModule
import importlib

def get_scripts(args: argparse.Namespace, path, target, scripts_mutable, root_parser, root_name, data):
    parser_subs = data.get_default('_'.join([*path, target])).get('subparsers')
    if not path:
        value = getattr(args, root_name)
    else:
        value = getattr(args, target)
        if value:
            cmd_target = '_'.join(path+[target, value])
            script = data.get_default(cmd_target).get('script')
            if script:
                scripts_mutable.append(script)
            return
    path = path + [target]
    if parser_subs and value is None:
        root_parser.parse_args(path[1:]+['-h'])
    elif parser_subs and value:
        subcmd = '_'.join(path+[value])
        script = data.get_default(subcmd).get('script')
        if script:
            scripts_mutable.append(script)
        get_scripts(args, path, value, scripts_mutable, root_parser, root_name, data)
        return

# 4. load and run scripts
def run(cfg):
    root_parser, root_name, data = build_root_parser(cfg)
    argcomplete.autocomplete(root_parser)
    scripts = []
    args, other_args = root_parser.parse_known_args()
    args.other_args = other_args
    get_scripts(args, [], 'root', scripts, root_parser, root_name, data)

    execution_context: dict[str, Any] = {}
    for script in scripts:
        mod = cast(
            SubcommandModule,
            importlib.import_module(f'{data['root']['script_dir']}.{script}')
        )        
        mod.run(args, execution_context)

def run_from_manifest(config_root):
    from .build_config import read_manifest, build_config
    config_paths = read_manifest(config_root)
    cfg = build_config(config_root, config_paths)
    run(cfg)