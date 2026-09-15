import gi
gi.require_version('Gtk', '3.0')
from pathlib import Path
from ui.app import Application
from models import Command
from sigil import Parser, Resolver
from sigil.datasource.yml_source import YmlSource


CALLER_SCRIPT = """
#!/usr/bin/python3
#PYTHON_ARGCOMPLETE_OK
from pathlib import Path
from multitool_lib import run_from_manifest

run_from_manifest(Path(__file__).parent)
"""

def reconstruct_configs(fileroot):
    cfg_root = Path(fileroot).parent
    parsed = Parser(YmlSource).load(cfg_root)
    resolved = Resolver.resolve_inheritance(parsed)
    reconstructed = Command.from_config('root',resolved, cfg_root=cfg_root)
    return reconstructed

def save_configs(root_cmd: Command, filepath: Path):
    # implement your YAML serialisation here
    root_cmd.update_internal_ids()
    if not root_cmd.script_dir:
        root_cmd.script_dir = 'scripts'
    filenames = root_cmd.write_tree(filepath)
    with open(filepath/'.manifest.yml', 'w') as f:
        f.writelines([
            f'- yml/{x}.yml\n'
            for x in filenames
        ])
    
    with open(filepath/f'{root_cmd.name}.py', 'w') as f:
        f.write(CALLER_SCRIPT)

if __name__ == "__main__":
    app = Application(reconstruct_configs, save_configs)
    app.run(None)