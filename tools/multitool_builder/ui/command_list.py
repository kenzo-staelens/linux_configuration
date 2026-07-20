from gi.repository import Gtk, Gdk, Pango
from models.command import Command
from models.argument import Argument
from models.script import Script


class CommandList(Gtk.ScrolledWindow):
    def __init__(self, on_row_activated, on_item_deleted):
        super().__init__()
        self.on_row_activated = on_row_activated
        self.on_item_deleted = on_item_deleted

        # ListStore: name, detail, object, type_str (unused)
        self.store = Gtk.ListStore(str, str, object, str)
        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.set_rules_hint(True)
        self.treeview.set_hexpand(True)                    # fill available width
        self.add(self.treeview)

        # --- Name column ---
        renderer_name = Gtk.CellRendererText()
        col_name = Gtk.TreeViewColumn("Name", renderer_name, text=0)
        col_name.set_resizable(True)
        col_name.set_expand(True)                          # stretch to fill space
        col_name.set_cell_data_func(renderer_name, self.name_data_func)
        self.treeview.append_column(col_name)

        # --- Detail column ---
        renderer_detail = Gtk.CellRendererText()
        col_detail = Gtk.TreeViewColumn("Detail", renderer_detail, text=1)
        col_detail.set_resizable(True)
        col_detail.set_expand(True)                        # stretch to fill space
        col_detail.set_cell_data_func(renderer_detail, self.detail_data_func)
        self.treeview.append_column(col_detail)

        # --- Delete column (no title) ---
        renderer_del = Gtk.CellRendererText()
        renderer_del.set_property("text", "✕")
        renderer_del.set_property("foreground", "red")
        renderer_del.set_property("weight", Pango.Weight.BOLD)
        col_del = Gtk.TreeViewColumn("", renderer_del)
        col_del.set_min_width(30)
        col_del.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        self.treeview.append_column(col_del)

        # Connect signals
        self.treeview.connect("row-activated", self.on_tree_row_activated)
        self.treeview.connect("button-press-event", self.on_button_press)
        self.treeview.get_selection().connect("changed", self.on_selection_changed)

    # ---------- Styling callbacks ----------
    def name_data_func(self, column, cell, model, iter, data):
        obj = model.get_value(iter, 2)
        if isinstance(obj, Command):
            cell.set_property("weight", Pango.Weight.BOLD)
            cell.set_property("foreground", "blue")
            cell.set_property("style", Pango.Style.NORMAL)
        elif isinstance(obj, Argument):
            cell.set_property("weight", Pango.Weight.BOLD)
            cell.set_property("foreground", "green")
            cell.set_property("style", Pango.Style.ITALIC)
        elif isinstance(obj, Script):
            cell.set_property("weight", Pango.Weight.BOLD)
            cell.set_property("foreground", "gray")
            cell.set_property("style", Pango.Style.NORMAL)

    def detail_data_func(self, column, cell, model, iter, data):
        # no extra styling required for detail column
        pass

    # ---------- Data population ----------
    def populate(self, command):
        self.store.clear()
        if command is None:
            return
        # 1. Arguments first
        for arg in command.children_args:
            self.store.append([arg.canonical_name, arg.name, arg, "argument"])
        # 2. Subcommands
        for sub in command.children_subcommands:
            self.store.append([sub.name, "", sub, "subcommand"])
        # 3. Script (max one)
        script = command.child_script
        if script:
            self.store.append([script.name, "<script>", script, "script"])
        self.treeview.get_selection().unselect_all()

    # ---------- Event handlers ----------
    def on_tree_row_activated(self, treeview, path, column):
        tree_iter = self.store.get_iter(path)
        obj = self.store.get_value(tree_iter, 2)
        self.on_row_activated(obj)

    def on_button_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            x, y = event.x, event.y
            result = widget.get_path_at_pos(int(x), int(y))
            if result is None:
                # Clicked on empty space – keep current command properties visible
                self.treeview.get_selection().unselect_all()
                toplevel = self.get_toplevel()
                if hasattr(toplevel, 'current_command'):
                    toplevel.detail_editor.set_object(toplevel.current_command)
                return False
            path, col, _, _ = result
            # Our delete column has an empty title
            if col and col.get_title() == "":
                tree_iter = self.store.get_iter(path)
                obj = self.store.get_value(tree_iter, 2)
                self.on_item_deleted(obj)
                return True
        return False

    def on_selection_changed(self, selection):
        model, tree_iter = selection.get_selected()
        toplevel = self.get_toplevel()
        if tree_iter:
            obj = model.get_value(tree_iter, 2)
        else:
            # Fall back to the current command being viewed (root or subcommand)
            obj = getattr(toplevel, 'current_command', None)

        if obj is not None and hasattr(toplevel, 'detail_editor'):
            toplevel.detail_editor.set_object(obj)
        elif hasattr(toplevel, 'detail_editor'):
            toplevel.detail_editor.clear()

    # ---------- Real‑time update helper ----------
    def update_object_row(self, obj):
        for row in self.store:
            if row[2] is obj:
                if isinstance(obj, Command):
                    row[0] = obj.name
                    row[1] = ""
                elif isinstance(obj, Argument):
                    row[0] = obj.canonical_name
                    row[1] = obj.name
                elif isinstance(obj, Script):
                    row[0] = obj.name
                    row[1] = "<script>"
                    row
                return
    
    def update_script_object(self, old, obj):
        for row in self.store:
            if row[2] is old:
                row[0] = obj.name
                row[2] = obj