import yaml
from .yaml_constructors import argument
from .helper import dictWrap

def read_manifest(config_root, manifest_file='.manifest.yml'):
    with open(config_root/manifest_file) as f:
        return yaml.load(f.read(), yaml.SafeLoader)

def build_config(config_root, config_paths):
    config = "---\n"
    for file in config_paths:
        with open(config_root/file) as f:
            config += f'{f.read()}\n'
    return config

def resolve_inheritance(config_data):
    # temporary used here for checking has resolved
    # as also storing "pointers" to nested objects
    resolved = {}
    changed = True
    while changed:
        changed = False
        for p_id, parser in config_data.items():
            if p_id in resolved:
                continue
            if not isinstance(parser, dict):
                continue
            changed = True
            parent = parser.get('parent')
            if parent:
                sub = resolved[parent].get('subparsers', {})
                sub[parser['name']]= parser
                resolved[parent]['subparsers'] = sub
            resolved[p_id] = parser
    return resolved['root']

def build_resolved(config_root, manifest_file='.manifest.yml'):
    paths = read_manifest(config_root, manifest_file)
    config = build_config(config_root, paths)
    yaml.SafeLoader.add_constructor(argument.Argument.yaml_tag, argument.Argument.from_yaml)
    data: dictWrap = dictWrap(yaml.load(config, Loader = yaml.SafeLoader))
    resolved = resolve_inheritance(data)
    return resolved