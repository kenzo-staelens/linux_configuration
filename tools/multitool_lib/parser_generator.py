import argcomplete
import yaml
from .build_config import resolve_inheritance
from multitool_lib.yaml_constructors import argument
from .helper import dictWrap, MyArgParser
from typing import Any

def build_subparsers(base_parser: MyArgParser, parser_data: dict[str, Any]):
    if parser_data.get('subparsers'):
        grp = base_parser.add_subparsers(dest=parser_data['name'], title='subcommands')
        last_default = None
        for k, subcommand in parser_data['subparsers'].items():
            subcommand_name = subcommand['name']
            subcmd_help = subcommand.get('help')
            subcmd = grp.add_parser(subcommand_name, help=subcmd_help)
            for arg in subcommand.get('args', []):
                arg.add_to_parser(subcmd)
            if subcommand.get('default', False):
                last_default = subcommand['name']
            if subcommand.get('subparsers'):
                build_subparsers(subcmd, subcommand)
        if last_default:
            base_parser.set_default_subparser(last_default)
                

def build_root_parser(config):
    yaml.SafeLoader.add_constructor(argument.Argument.yaml_tag, argument.Argument.from_yaml)
    data: dictWrap = dictWrap(yaml.load(config, Loader = yaml.SafeLoader))
    resolved = resolve_inheritance(data)

    root_name = resolved['name']
    root_parser = MyArgParser(prog=root_name)

    for arg in resolved.get('args', []) or []:
        arg.add_to_parser(root_parser)

    build_subparsers(root_parser, resolved)
    argcomplete.autocomplete(root_parser)
    return root_parser, root_name, resolved
