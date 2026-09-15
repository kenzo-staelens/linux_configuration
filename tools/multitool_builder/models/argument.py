import yaml
from typing import Any
from .property import Property

class Argument:
    def __init__(self, names=[], action="", help="", required=False, default=None, properties=None):
        self.name = ','.join(names)               # comma separated
        self.canonical_name = self.compute_canonical()  # computed property
        self.action = action
        self.help: str = help
        self.required = required
        self.default = default
        self.properties: list[Property] = [] if properties is None else properties

    def compute_canonical(self):
        return self.name.split(",")[0].strip() if self.name else ""

    @classmethod
    def _get_properties(cls, arg_data):
        return [
            Property(k, str(v))
            for k,v in arg_data.items()
        ]
    
    @classmethod
    def from_config(cls, args):
        parser_args = [
            cls(
                getattr(arg,'name', None), 
                getattr(arg,'action', None),
                getattr(arg,'help', None),
                getattr(arg,'required', None),
                getattr(arg,'default', None),
                cls._get_properties(
                    getattr(arg, 'kw', {})
                )
            )
            for arg in args
        ]
        return parser_args

    def to_config(self):
        data: dict[str, Any] = {
            'name': [x.strip() for x in self.name.split(',')]
        }
        if self.default:
            data['default'] = self.default
        if self.help:
            data['help'] = self.help
        if self.action:
            data['action'] = self.action
        for property in self.properties:
            data[property.name] = property.value
        return data

def arg_representer(dumper, obj):
    data = obj.to_config()
    return dumper.represent_mapping('!arg', data)

yaml.add_representer(Argument, arg_representer)

