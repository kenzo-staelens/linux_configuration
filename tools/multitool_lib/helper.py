#!/usr/bin/python3
import argparse
import sys
from typing import Any, TypedDict
from types import ModuleType
from multitool_lib.yaml_constructors import argument

class ParserContext(TypedDict):
    id: str
    name: str
    args: list[argument.Argument]
    subparsers: list[str]

class SubcommandModule(ModuleType):
    @staticmethod
    def run(args: argparse.Namespace, ctx: dict[str, Any]): ...

class Stack:
    def __init__(self):
        self.content = []
    
    def __bool__(self):
        return len(self.content)>0

    def push(self, value):
        self.content.append(value)
    
    def pop(self):
        if len(self.content)==0:
            return None
        self.content, val = self.content[:-1], self.content[-1]
        return val 

class dictWrap(dict):
    def get_default(self, key: str, default=None):
        if not default:
            default = dictWrap()
        v = self.get(key, default) or default
        if isinstance(v, dict):
            return dictWrap(v)
        return v

class MyArgParser(argparse.ArgumentParser):
    # https://stackoverflow.com/a/26379693/11380911
    def set_default_subparser(self, name, args=None, positional_args=0):
        """default subparser selection. Call after setup, just before parse_args()
        name: is the name of the subparser to call by default
        args: if set is the argument list handed to parse_args()

        , tested with 2.7, 3.2, 3.3, 3.4
        it works with 2.6 assuming argparse is installed
        """
        subparser_found = False
        existing_default = False # check if default parser previously defined
        for arg in sys.argv[1:]:
            if arg in ['-h', '--help']:  # global help if no subparser
                break
        else:
            for x in self._subparsers._actions:
                if not isinstance(x, argparse._SubParsersAction):
                    continue
                for sp_name in x._name_parser_map.keys():
                    if sp_name in sys.argv[1:]:
                        subparser_found = True
                    if sp_name == name: # check existance of default parser
                        existing_default = True
            if not subparser_found:
                # If the default subparser is not among the existing ones,
                # create a new parser.
                # As this is called just before 'parse_args', the default
                # parser created here will not pollute the help output.

                if not existing_default:
                    for x in self._subparsers._actions:
                        if not isinstance(x, argparse._SubParsersAction):
                            continue
                        x.add_parser(name)
                        break # this works OK, but should I check further?

                # insert default in last position before global positional
                # arguments, this implies no global options are specified after
                # first positional argument
                if args is None:
                    sys.argv.insert(len(sys.argv) - positional_args, name)
                else:
                    args.insert(len(args) - positional_args, name)

type parserdict = 'dict[str, MyArgParser]'