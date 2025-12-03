import argcomplete
import yaml
from .build_config import resolve_inheritance
from multitool_lib.yaml_constructors import argument
from .helper import dictWrap, Stack, parserdict, ParserContext, MyArgParser


def build_root_parser(config):
    yaml.SafeLoader.add_constructor(argument.Argument.yaml_tag, argument.Argument.from_yaml)
    data: dictWrap = dictWrap(yaml.load(config, Loader = yaml.SafeLoader))
    resolve_inheritance(data)

    root_name = data['root']['name']
    root_parser = MyArgParser(prog=root_name)

    current_path = Stack()
    current_path.push('root')
    parsers: parserdict = {'root': root_parser}

    def get_current_parser_ctx() -> tuple[MyArgParser, ParserContext]:
        current_name: str = current_path.pop()
        current_parser: MyArgParser = parsers[current_name]

        current_data: dictWrap = data.get_default(current_name)
        subcmd_args: list[argument.Argument] = current_data.get_default('args', [])
        subcmd_subparsers: list[str] = current_data.get_default('subparsers', [])
        subcmd_name: list[str] = current_data.get_default('name', current_name)

        return (
            current_parser,
            {
                'id':current_name,
                'name': subcmd_name,
                'args': subcmd_args,
                'subparsers': subcmd_subparsers,
            }
        )

    while current_path:
        parser, parser_ctx = get_current_parser_ctx()
        for arg in parser_ctx['args']:
            arg.add_to_parser(parser)

        if len(parser_ctx['subparsers']):
            grp = parser.add_subparsers(dest=parser_ctx['name'], title='subcommands')
            last_default = None
            for subcommand in parser_ctx['subparsers']:
                subcmd_name = data[subcommand]['name']
                subcmd_help = data[subcommand].get('help')
                subcmd = grp.add_parser(subcmd_name, help=subcmd_help)
                if data[subcommand].get('default'):
                    last_default = data[subcommand]['name']
                parsers[subcommand] = subcmd 
                current_path.push(subcommand)
            # first add all arguments
            # then attempt to set the default
            # otherwise cases exist where parse_args will attempt to add the default
            # when another is already selected (but not yet defined)
            if last_default:
                parser.set_default_subparser(last_default)
    argcomplete.autocomplete(root_parser)
    return root_parser, root_name, data