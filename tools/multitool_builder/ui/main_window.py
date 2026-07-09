from gi.repository import Gtk, Gio
from .breadcrumb import Breadcrumb
from .command_list import CommandList
from .detail_editor import DetailEditor
from models import Command, Argument, Script
from pathlib import Path


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, loader, saver):
        super().__init__(title="Command Editor")
        self.loader = loader
        self.saver = saver
        self.root_command = None
        self.current_command = None
        self.filepath = None

        self.set_default_size(1000, 700)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        self.add(vbox)

        # Toolbar
        tb = Gtk.Box(spacing=6)
        vbox.pack_start(tb, False, False, 0)

        # New
        btn_new = Gtk.Button.new_from_icon_name("document-new", Gtk.IconSize.BUTTON)
        btn_new.set_tooltip_text("New project")
        btn_new.connect("clicked", lambda w: self._new())
        tb.pack_start(btn_new, False, False, 0)

        # Load
        btn_load = Gtk.Button.new_from_icon_name("document-open", Gtk.IconSize.BUTTON)
        btn_load.set_tooltip_text("Load YAML")
        btn_load.connect("clicked", self.on_load)
        tb.pack_start(btn_load, False, False, 0)

        # Save
        self.btn_save = Gtk.Button.new_from_icon_name("media-floppy", Gtk.IconSize.BUTTON)
        if not self.btn_save.get_image():
            self.btn_save = Gtk.Button.new_from_icon_name("document-save", Gtk.IconSize.BUTTON)
        self.btn_save.set_tooltip_text("Save")
        self.btn_save.connect("clicked", self.on_save)
        tb.pack_start(self.btn_save, False, False, 0)

        # Save As
        self.btn_save_as = Gtk.Button.new_from_icon_name("document-save-as", Gtk.IconSize.BUTTON)
        self.btn_save_as.set_tooltip_text("Save As...")
        self.btn_save_as.connect("clicked", self.on_save_as)
        tb.pack_start(self.btn_save_as, False, False, 0)

        # Breadcrumb
        self.breadcrumb = Breadcrumb(self._on_breadcrumb_clicked)
        tb.pack_start(self.breadcrumb, True, True, 0)

        # Add buttons (right)
        add_box = Gtk.Box(spacing=3)
        tb.pack_end(add_box, False, False, 0)

        self.btn_add_sub = Gtk.Button(label="Add Subcommand")
        self.btn_add_sub.connect("clicked", lambda w: self._add(Command, "sub"))
        add_box.pack_start(self.btn_add_sub, False, False, 0)

        self.btn_add_arg = Gtk.Button(label="Add Argument")
        self.btn_add_arg.connect("clicked", lambda w: self._add(Argument, "arg"))
        add_box.pack_start(self.btn_add_arg, False, False, 0)

        self.btn_add_script = Gtk.Button(label="Add Script")
        self.btn_add_script.connect("clicked", lambda w: self._add_script())
        add_box.pack_start(self.btn_add_script, False, False, 0)

        # Main area
        self.command_list = CommandList(self._on_row_activated, self._on_item_deleted)
        vbox.pack_start(self.command_list, True, True, 0)

        self.detail_editor = DetailEditor()
        self.detail_editor.connect('property-changed', self._on_property_changed)
        self.detail_editor.connect('property-changed-obj', self._on_property_changed_obj)
        self.detail_editor.set_size_request(-1, 250)
        vbox.pack_start(self.detail_editor, False, False, 0)

        self._update_ui()

    # -------- internal helpers --------
    def _update_ui(self):
        active = self.root_command is not None
        self.btn_save.set_sensitive(active)
        self.btn_save_as.set_sensitive(active)
        self.btn_add_sub.set_sensitive(active)
        self.btn_add_arg.set_sensitive(active)
        self.btn_add_script.set_sensitive(active and self.current_command and self.current_command.child_script is None)
        self.command_list.populate(self.current_command)
        if self.current_command:
            path = []
            cmd = self.current_command
            while cmd:
                path.append(cmd)
                cmd = getattr(cmd, '_ui_parent', None)
            path.reverse()
            self.breadcrumb.set_path(path)
            self.detail_editor.set_command(self.current_command)
        else:
            self.breadcrumb.set_path([])

    def _new(self):
        self.root_command = Command(name="root")
        self.root_command.is_root = True
        self.current_command = self.root_command
        self.filepath = None
        self._update_ui()

    def _on_breadcrumb_clicked(self, cmd):
        self.current_command = cmd
        self._update_ui()

    def _on_row_activated(self, obj):
        if isinstance(obj, Command):
            obj._ui_parent = self.current_command
            self.current_command = obj
            self._update_ui()

    def _on_item_deleted(self, obj):
        if isinstance(obj, Argument):
            self.current_command.children_args.remove(obj)
        elif isinstance(obj, Command):
            self.current_command.children_subcommands.remove(obj)
        elif isinstance(obj, Script):
            self.current_command.child_script = None
        self._update_ui()
        self.detail_editor.clear()

    def _on_property_changed(self, editor, obj):
        self.command_list.update_object_row(obj)

    def _on_property_changed_obj(self, editor, objs):
        old, obj = objs
        self.command_list.update_script_object(old, obj)

    def _add(self, cls, kind):
        if not self.current_command:
            return
        if kind == "sub":
            cmd = Command(name="new_subcommand")
            cmd._ui_parent = self.current_command
            cmd.parent = self.current_command.internal_id
            self.current_command.children_subcommands.append(cmd)
        elif kind == "arg":
            self.current_command.children_args.append(Argument(["--arg"]))
        self._update_ui()

    def _add_script(self):
        if self.current_command and self.current_command.child_script is None:
            self.current_command.child_script = Script(name="new_script")
            self._update_ui()

    # -------- file i/o callbacks --------
    def on_load(self, widget):
        dlg = Gtk.FileChooserDialog("Open YAML", self, Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        f = Gtk.FileFilter()
        f.set_name("YAML")
        f.add_pattern("*.yml")
        f.add_pattern("*.yaml")
        dlg.add_filter(f)
        if dlg.run() == Gtk.ResponseType.OK:
            self.filepath = dlg.get_filename()
            self.root_command = self.loader(self.filepath)
            self.current_command = self.root_command
            self._update_ui()
        dlg.destroy()

    def on_save(self, widget):
        if not self.root_command:
            return
        if not self.filepath:
            self._save_as()
        else:
            target_dir = Path(self.filepath).parent
            self.saver(self.root_command, target_dir)

    def on_save_as(self, widget):
        if not self.root_command:
            return
        self._save_as()

    def _save_as(self):
        dlg = Gtk.FileChooserDialog(
            "Select Directory to Save project",
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        filter = Gtk.FileFilter()
        filter.set_name("Folders only")

        def _show_only_dirs(filter_info):
            # filter_info is a Gtk.FileFilterInfo
            try:
                # Convert URI to local path
                path = Gio.File.new_for_uri(filter_info.uri).get_path()
                # Return True only if it's a directory (or fails safe)
                import os
                return path is not None and os.path.isdir(path)
            except Exception:
                return False
        filter.add_custom(Gtk.FileFilterFlags.URI, _show_only_dirs)
        dlg.add_filter(filter)
        dlg.set_filter(filter)
        dlg.set_do_overwrite_confirmation(True)

        if dlg.run() == Gtk.ResponseType.OK:
            chosen_path = dlg.get_filename()
            # Always save as <chosen_directory>/.manifest.yml
            target_dir = Path(chosen_path)
            self.filepath = target_dir / '.manifest.yml'
            if not self.root_command.script_dir.startswith('/'):
                self.root_command.script_dir = None  # force local scripts for save as
            self.saver(self.root_command, target_dir)
        dlg.destroy()