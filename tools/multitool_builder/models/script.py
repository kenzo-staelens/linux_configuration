from pathlib import Path
from collections import defaultdict

SCRIPT_DEFAULT = """
from argparse import Namespace
from typing import Any

def run(args: Namespace, ctx: dict[str, Any]):
    pass
""".lstrip()

class Script:
    def __init__(self, name="", content=""):
        self.name = name
        self.content = content

    @classmethod
    def from_config(cls, script_dir, scriptname):
        if scriptname in SCRIPT_REF:
            return SCRIPT_REF[scriptname]
        if not script_dir:
            return None
        with open(Path(script_dir)/(scriptname + '.py')) as f:
            script_data = f.read()
        sc = Script(scriptname, script_data)
        SCRIPT_REF[scriptname] = sc  # shared reference
        return sc

    def write(self, fileroot):
        directory = Path(fileroot)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        with open(directory/f'{self.name}.py', 'w') as f:
            f.write(self.content)

class CustomDefaultdict(defaultdict):
    def __missing__(self, key):
        obj = Script(name=key, content=SCRIPT_DEFAULT)
        dict.__setitem__(self, key, obj)
        return self[key]

SCRIPT_REF = CustomDefaultdict()
