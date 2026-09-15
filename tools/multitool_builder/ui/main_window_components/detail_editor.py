from ui.ui_builders import ScriptBuilder, ArgumentBuilder, CommandBuilder, PropertyBuilder


class DetailEditor(ArgumentBuilder, CommandBuilder, ScriptBuilder, PropertyBuilder):
    def __init__(self):
        super().__init__(label="Properties")