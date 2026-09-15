from gi.repository import Pango
from ui.main_window_components.class_dispatchable import ClassDispatchable
# from .list_renderer_base import ListRendererBase
from models import Argument

class ArgumentListRenderer(ClassDispatchable):
    object_class = Argument
    is_navigatable = True

    @classmethod
    def name_data_func(cls, cell):
        cell.set_property("weight", Pango.Weight.BOLD)
        cell.set_property("foreground", "green")
        cell.set_property("style", Pango.Style.ITALIC)

    @classmethod
    def _populate(cls, obj: Argument):
        return [
            cls.create_entry(item.name, item.value, item, "property")
            for item in obj.properties
        ]
        
    @classmethod
    def update_object_row(cls, row, obj):
        row[0] = obj.canonical_name
        row[1] = obj.name
