from .field_builder import FieldBuilder
from models import Argument

class ArgumentBuilder(FieldBuilder):
    def build_argument_editor(self, arg: Argument):
        # Row 0: names + action (action may be None)
        self._add_field(0, 0, "names", arg.names, self.on_arg_names_changed, arg)
        self._add_field(0, 2, "action", arg.action, self.on_arg_action_changed, arg)
        # Row 1: help + required
        self._add_field(1, 0, "help", arg.help, self.on_arg_help_changed, arg)
        self._add_bool_field(1, 2, "required", arg.required, self.on_arg_required_changed, arg)
        # Row 2: default (bool)
        self._add_field(2, 0, "default", getattr(arg, 'default', ''), self.on_arg_default_changed, arg)

    def set_object(self, obj):
        super().set_object(obj)
        if isinstance(obj, Argument):
            self.build_argument_editor(obj)
        self.show_all()

    def on_arg_names_changed(self, entry, arg: Argument):
        arg.names = entry.get_text()
        arg.canonical_name = arg.compute_canonical()
        self.emit_property_changed(arg)

    def on_arg_action_changed(self, entry, arg: Argument):
        arg.action = entry.get_text() or None  # keep None if empty
        self.emit_property_changed(arg)

    def on_arg_help_changed(self, entry, arg: Argument):
        arg.help = entry.get_text()
        self.emit_property_changed(arg)

    def on_arg_required_changed(self, check, arg: Argument):
        arg.required = check.get_active()
        self.emit_property_changed(arg)

    def on_arg_default_changed(self, check, arg: Argument):
        arg.default = check.get_text()
        self.emit_property_changed(arg)
