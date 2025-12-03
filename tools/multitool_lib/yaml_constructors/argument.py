import yaml
from typing import Self
import argparse
from typing import Any


class Argument(yaml.YAMLObject):
    yaml_tag = u'!arg'

    def __init__(
        self, 
        name: list[str], 
        help: str="", 
        action: str | None=None,
        required: bool=False,
        completer: Any = None,
        **kw
    ):
        self.names = name
        self.help = help
        self.action= action
        self.required= required
        self.kw = kw
    
    def __repr__(self):
        return 'Argument({})'.format(str(self.names))

    @classmethod
    def from_yaml(cls, loader: yaml.Loader, node: yaml.MappingNode):
        content = loader.construct_mapping(node, deep=True)
        return Argument(**content)

    @classmethod
    def to_yaml(cls, dumper: yaml.Dumper, obj: Self):
        return dumper.represent_mapping(
            cls.yaml_tag,
            obj.names
        )

    def add_to_parser(self, parser: argparse.ArgumentParser):
        
        conditional_args = {}
        if any(x.startswith('-') for x in self.names):
            conditional_args['required']=self.required
        parser.add_argument(
            *self.names,
            help=self.help,
            action=self.action,
            **(self.kw | conditional_args)
        )