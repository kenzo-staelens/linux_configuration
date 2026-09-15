from gi.repository import Pango
from ui.main_window_components.class_dispatchable import ClassDispatchable
from models import Command

class CommandListRenderer(ClassDispatchable):
    object_class = Command
    is_navigatable = True

    @classmethod
    def name_data_func(self, cell):
        cell.set_property("weight", Pango.Weight.BOLD)
        cell.set_property("foreground", "blue")
        cell.set_property("style", Pango.Style.NORMAL)

    @classmethod
    def _populate(cls, obj: Command):
        added_data = []
        # 1. Arguments first
        for arg in obj.children_args:
            added_data.append(cls.create_entry(
                arg.canonical_name, arg.name, arg, "argument"
            ))
        # 2. Subcommands
        for sub in obj.children_subcommands:
            added_data.append(cls.create_entry(
                sub.name, "", sub, "subcommand"
            ))
        # 3. Script (max one)
        script = obj.child_script
        if script:
            added_data.append(cls.create_entry(
                script.name, "<script>", script, "script"
            ))
        return added_data

    @classmethod
    def update_object_row(cls, row, obj):
        row[0] = obj.name
        row[1] = ""