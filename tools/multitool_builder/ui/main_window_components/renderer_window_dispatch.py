from .class_dispatchable import DISPATCHABLE_OBJECTS, ClassDispatchable

class CommandListDispatch():
    @classmethod
    def _class_dispatcher(cls, obj):
        return DISPATCHABLE_OBJECTS.get(
            type(obj),
            ClassDispatchable
        )

    # ---------- Styling callbacks ----------
    def name_data_func(self, column, cell, model, iter, data):
        obj = model.get_value(iter, 2)
        renderer = self._class_dispatcher(obj)
        renderer.name_data_func(cell)

    def detail_data_func(self, column, cell, model, iter, data):
        # no extra styling required for detail column
        pass

    # ---------- Data population ----------
    def populate(self, obj):
        renderer = self._class_dispatcher(obj)
        renderer.populate(self.store, self.treeview, obj)

    # ---------- Real‑time update helper ----------
    def update_object_row(self, obj):
        renderer = self._class_dispatcher(obj)
        for row in self.store:
            if row[2] is obj:
                renderer.update_object_row(row, obj)
                return

    def update_object_row_object(self, old, obj):
        renderer = self._class_dispatcher(obj)
        for row in self.store:
            if row[2] is obj:
                renderer.update_object_row_object(row, old, obj)
                return
            