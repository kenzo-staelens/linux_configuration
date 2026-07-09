from .ui_builders import ScriptBuilder, ArgumentBuilder, CommandBuilder


class DetailEditor(ArgumentBuilder, CommandBuilder, ScriptBuilder):
    def __init__(self):
        super().__init__(label="Properties")