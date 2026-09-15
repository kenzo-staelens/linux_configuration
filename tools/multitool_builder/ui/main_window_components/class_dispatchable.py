from gi.repository import Pango

DISPATCHABLE_OBJECTS: 'dict[object, type[ClassDispatchable]]' = {}

class ClassDispatchable:
    object_class: type | None = None
    is_navigatable = False

    @classmethod
    def register(cls):
        if not cls.object_class:
            raise TypeError('missing object class')
        print(f'registered {cls.__name__}')
        DISPATCHABLE_OBJECTS[cls.object_class] = cls

    @classmethod
    def populate(cls, store, treeview, obj):
        if obj is None:
            return
        store.clear()
        for item in cls._populate(obj):
            store.append(item)
        treeview.get_selection().unselect_all()

    @classmethod
    def _populate(cls, obj):
        raise NotImplementedError(f'populate Not implemented for class {cls.object_class.__name__}')

    @classmethod
    def update_object_row(cls, row, obj):
        # replace properties of object
        raise NotImplementedError(f'update_object_row Not implemented for class {cls.object_class.__name__}')        

    @classmethod
    def update_object_row_object(cls, row, obj):
        # replace object
        raise NotImplementedError(f'update_object_row_object Not implemented for class {cls.object_class.__name__}')        


    @classmethod
    def name_data_func(cls, cell):
        # default
        cell.set_property("weight", Pango.Weight.BOLD)
        cell.set_property("foreground", "black")
        cell.set_property("style", Pango.Style.NORMAL)

    @classmethod
    def create_entry(cls, name, detail, item, o_type):
        # mostly a sanity check thing
        return [name, detail, item, o_type]

    @classmethod
    def delete_record(cls, current_obj, del_obj):
        raise NotImplementedError(f'delete_record Not implemented for class {cls.object_class.__name__}')

    @classmethod
    def _add(cls):
        raise NotImplementedError(f'_add Not implemented for class {cls.object_class.__name__}')