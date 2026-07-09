#!/usr/bin/python3
import argparse
from typing import Any, TypedDict
from types import ModuleType
from multitool_lib.yaml_constructors import argument

class ParserContext(TypedDict):
    id: str
    name: str
    args: list[argument.Argument]
    subparsers: dict[str, str]

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
    def set_default_subparser(self, name, args=None, positional_args=0):
        for action in self._actions:
            if not isinstance(action, argparse._SubParsersAction):
                continue
            if name in action._name_parser_map.keys():
                action.default=name
        
type parserdict = 'dict[str, MyArgParser]'