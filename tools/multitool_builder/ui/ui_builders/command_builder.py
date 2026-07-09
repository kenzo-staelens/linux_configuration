from .field_builder import FieldBuilder
from models import Command

class CommandBuilder(FieldBuilder):

    def build_command_editor(self, cmd: Command):
        if getattr(cmd, 'is_root', False):
            self._build_root_command_editor(cmd)
            return
        # existing code for normal commands stays unchanged
        self._add_field(0, 0, "name", cmd.name, self.on_cmd_name_changed, cmd)
        self._add_field(0, 2, "help", getattr(cmd, 'help', ''), self.on_cmd_help_changed, cmd)
        self._add_bool_field(1, 0, "default", cmd.default, self.on_cmd_default_changed, cmd)

    def set_object(self, obj):
        super().set_object(obj)
        if isinstance(obj, Command):
            self.build_command_editor(obj)
        self.show_all()

    def _build_root_command_editor(self, cmd: Command):
        # Only name for the root (adjust as needed)
        self._add_field(0, 0, "name", cmd.name, self.on_cmd_name_changed, cmd)
        self._add_field(0, 2, "script dir", cmd.script_dir, self.on_scriptdir_name_changed, cmd)

    def on_cmd_name_changed(self, entry, cmd: Command):
        cmd.name = entry.get_text()
        self.emit_property_changed(cmd)
    
    def on_scriptdir_name_changed(self, entry, cmd: Command):
        cmd.set_scriptdir(entry.get_text())
        self.emit_property_changed(cmd)

    def on_cmd_help_changed(self, entry, cmd: Command):
        cmd.help = entry.get_text()
        self.emit_property_changed(cmd)

    def on_cmd_default_changed(self, entry, cmd: Command):
        cmd.default = entry.get_active()
        self.emit_property_changed(cmd)