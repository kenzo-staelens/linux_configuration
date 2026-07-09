from .argument import Argument
from .script import Script
import yaml
from pathlib import Path
from typing import cast

class Command:
    def __init__(self, internal_id="", name="", script="", parent=None, help_str="", default=False):
        self.internal_id = internal_id
        self.name = name
        self.script = script             # plain string
        self.parent = parent             # internal_id of parent
        self.children_args: list[Argument] = []          # list[Argument]
        self.children_subcommands: list[Command] = []   # list[Command]
        self.child_script: Script | None = None         # Script or None
        self.help = help_str
        self.default = default
        self.is_root = False
        self.script_dir = None

    def update_internal_ids(self):
        if self.internal_id is None and self.parent is None:
            self.internal_id = 'root'

        if self.internal_id != 'root':
            self.internal_id = cast(str, self.parent) + '_' + self.name
            
        for cmd in self.children_subcommands:
            cmd.parent = self.internal_id
            cmd.update_internal_ids()

    def set_scriptdir(self, new_dir):
        self.script_dir = new_dir
        for cmd in self.children_subcommands:
            cmd.set_scriptdir(new_dir)

    @classmethod
    def from_config(cls, p_id, cfg, script_dir: str | None=None, cfg_root: Path | None =None, parent=None):
        root_parser = cls(
            p_id,
            cfg['name'],
            parent=parent,
            help_str=cfg.get('help'),
            default=cfg.get('default')
        )
        if parent is None:
            script_dir = cfg['script_dir']
            root_parser.is_root = True
        root_parser.script_dir = script_dir
        if sub := cfg.get('subparsers'):
            parsers = [
                cls.from_config(sp_id, parser_data, script_dir, cfg_root, p_id)
                for sp_id, parser_data in sub.items()
            ]
            root_parser.children_subcommands = parsers
    
        if args := cfg.get('args'):
            parser_args = Argument.from_config(args)
            root_parser.children_args = parser_args

        if script:=cfg.get('script'):
            sc = Script.from_config(cfg_root/script_dir, script)
            root_parser.script = script
            root_parser.child_script = sc
        return root_parser

    def collect_representations(self) -> list:
        res = [
            (self.internal_id, self.represent_self()),
        ]
        for cmd in self.children_subcommands:
            res += cmd.collect_representations()
        return res

    def write_scripts(self, fileroot: Path, default_path):
        script_path = fileroot/default_path
        if self.script_dir:
            script_path = fileroot/self.script_dir
        if self.child_script:
            self.child_script.write(script_path)
        for cmd in self.children_subcommands:
            cmd.write_scripts(fileroot, default_path)

    def represent_self(self):
        data = {
            'name': self.name,
        }
        if self.script:
            data['script'] = self.script
        if self.parent:
            data['parent'] = self.parent
        if self.help:
            data['help'] = self.help
        if self.default:
            data['default'] = self.default
        if self.children_args:
            data['args'] = self.children_args
        if self.script_dir and self.is_root:
            data['script_dir'] = self.script_dir
        return {self.internal_id: data}

    def write_tree(self, fileroot: str):
        reprs  = self.collect_representations()
        manifest_files = []
        for metadata, repr in reprs:
            ymldump = yaml.dump(repr, default_flow_style=False)
            self.write(ymldump, fileroot, metadata)
            manifest_files.append(metadata)

        self.write_scripts(Path(fileroot), 'scripts')
        return manifest_files

    def write(self, ymldump, fileroot, name):
        directory = Path(fileroot)/'yml'
        path = Path(fileroot)/'yml'/f'{name}.yml'
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(ymldump)
        return str(path)