from .class_dispatchable import DISPATCHABLE_OBJECTS, ClassDispatchable
from gi.repository import Gtk

class MainWindowDispatch(Gtk.ApplicationWindow):
    @classmethod
    def _class_dispatcher(cls, obj):
        return DISPATCHABLE_OBJECTS.get(
            type(obj),
            ClassDispatchable
        )

    def _on_row_activated(self, obj):
        dispatched = self._class_dispatcher(obj)
        if dispatched.is_navigatable:
            obj._ui_parent = self.current_command
            self.current_command = obj
            self._update_ui()
    
    def _on_item_deleted(self, obj):
        dispatched = self._class_dispatcher(obj)
        dispatched._on_item_deleted(obj)
        self._update_ui()
        self.detail_editor.clear()

    def _add(self, cls: type[ClassDispatchable]):
        if not self.current_command:
            return
        cls._add()
        self._update_ui()

    def _on_property_changed(self, editor, obj):
        self.command_list.update_object_row(obj)
     
    def _on_property_changed_obj(self, editor, objs):
        old, obj = objs
        self.command_list.update_object_row_object(old, obj)