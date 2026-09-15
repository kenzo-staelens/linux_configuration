from gi.repository import Pango
# from .list_renderer_base import ListRendererBase
from ui.main_window_components.class_dispatchable import ClassDispatchable
from models import Script

class ScriptListRenderer(ClassDispatchable):
    object_class = Script

    @classmethod
    def name_data_func(cls, cell):
        cell.set_property("weight", Pango.Weight.BOLD)
        cell.set_property("foreground", "gray")
        cell.set_property("style", Pango.Style.NORMAL)

    @classmethod
    def update_object_row(cls, row, obj):
        row[0] = obj.name
        row[1] = "<script>"

    @classmethod
    def update_object_row_object(cls, row, old, obj):
        row[0] = obj.name
        row[2] = obj