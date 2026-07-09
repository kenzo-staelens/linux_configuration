import yaml
from typing import Any

class Argument:
    def __init__(self, names=[], action="", help="", required=False, default=None):
        self.names = ','.join(names)               # comma separated
        self.canonical_name = self.compute_canonical()  # computed property
        self.action = action
        self.help: str = help
        self.required = required
        self.default = default

    def compute_canonical(self):
        return self.names.split(",")[0].strip() if self.names else ""
    
    @classmethod
    def from_config(cls, args):
        parser_args = [
            cls(
                arg.names, 
                arg.action,
                arg.help,
                arg.required,
                arg.default
            )
            for arg in args
        ]
        return parser_args

    def to_config(self):
        data: dict[str, Any] = {
            'name': [x.strip() for x in self.names.split(',')]
        }
        if self.default:
            data['default'] = self.default
        if self.help:
            data['help'] = self.help
        if self.action:
            data['action'] = self.action
        return data

def arg_representer(dumper, obj):
    data = obj.to_config()
    return dumper.represent_mapping('!arg', data)

yaml.add_representer(Argument, arg_representer)

