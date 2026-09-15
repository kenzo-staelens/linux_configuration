from .field_builder import FieldBuilder
from models import Property

class PropertyBuilder(FieldBuilder):
    def build_property_editor(self, prop: Property):
        self._add_field(0, 0, "name", prop.name, self.on_prop_name_changed, prop)
        self._add_field(0, 2, "value", prop.value, self.on_prop_value_changed, prop)
        
    def set_object(self, obj):
        super().set_object(obj)
        if isinstance(obj, Property):
            self.build_property_editor(obj)
        self.show_all()

    def on_prop_name_changed(self, entry, prop: Property):
        prop.name = entry.get_text()
        self.emit_property_changed(prop)

    def on_prop_value_changed(self, entry, prop: Property):
        prop.value = entry.get_text() or None  # keep None if empty
        self.emit_property_changed(prop)
