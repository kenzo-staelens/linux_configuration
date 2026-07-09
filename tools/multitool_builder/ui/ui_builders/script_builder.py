from .field_builder import FieldBuilder
from models.script import Script, SCRIPT_REF
from models.command import Command


class ScriptBuilder(FieldBuilder):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.current_command = None

    def build_script_editor(self, script):
        self._add_field(0, 0, "name", script.name, self.on_script_name_changed, script)
        self._add_multiline_field(1, 0, "content", script.content, self.on_script_content_changed, script)

    def set_object(self, obj):
        super().set_object(obj)
        if isinstance(obj, Script):
            self.build_script_editor(obj)
        self.show_all()

    def on_script_name_changed(self, entry, script: Script):
        # mostly managing state change to new script
        name = entry.get_text()
        sc: Script = SCRIPT_REF[name]
        self.current_command.script = sc
        self.current_command.child_script = sc
        text = sc.content
        self.current_object = sc

        self.emit_property_changed_obj(script, sc)
        self._widgets[id(script)]['content'].destroy()
        self.build_script_editor(sc)
        self._widgets[id(sc)]['content'].get_buffer().set_text(text if text else "")
        self.show_all()
        self.emit_property_changed(sc)
    
    def on_script_content_changed(self, buffer, script: Script):
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        script.content = buffer.get_text(start, end, True)
        self.emit_property_changed(script)

    def set_command(self, obj: Command):
        self.current_command = obj