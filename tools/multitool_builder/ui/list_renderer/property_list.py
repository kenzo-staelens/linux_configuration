from gi.repository import Pango
# from .list_renderer_base import ListRendererBase
from ui.main_window_components.class_dispatchable import ClassDispatchable
from models import Property

class PropertyListRenderer(ClassDispatchable):
    object_class = Property

    @classmethod
    def name_data_func(cls, cell):
        # same as script
        cell.set_property("weight", Pango.Weight.BOLD)
        cell.set_property("foreground", "gray")
        cell.set_property("style", Pango.Style.NORMAL)

    @classmethod
    def update_object_row(cls, row, obj: Property):
        row[0] = obj.name
        row[1] = obj.value
