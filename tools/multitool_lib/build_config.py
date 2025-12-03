import yaml

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
    for p_id, parser in config_data.items():
        if not isinstance(parser, dict):
            continue
    for p_id, parser in config_data.items():
        if not isinstance(parser, dict):
            continue
        parent = parser.get('parent')
        if parent:
            sub = config_data[parent].get('subparsers', [])
            sub.append(p_id)
            config_data[parent]['subparsers'] = sub
