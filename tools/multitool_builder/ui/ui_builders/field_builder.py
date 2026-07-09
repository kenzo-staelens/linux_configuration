import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango  # noqa: E402

# Try to load GtkSourceView for syntax highlighting
try:
    gi.require_version('GtkSource', '3.0')
    from gi.repository import GtkSource
    HAS_SOURCEVIEW = True
except (ValueError, ImportError):
    HAS_SOURCEVIEW = False


class FieldBuilder(Gtk.Frame):
    __gsignals__ = {
        'property-changed': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'property-changed-obj': (GObject.SIGNAL_RUN_FIRST, None, (object,))
    }

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._widgets = {}
        self.grid = None
        self.rebuild_grid()
        self.current_object = None
    
    def clear(self):
        self.rebuild_grid()
        self._widgets.clear()
        self.current_object = None

    def set_object(self, obj):
        self.clear()
        self.current_object = obj
    
    def rebuild_grid(self):
        if self.grid:
            self.remove(self.grid)
        self.grid = Gtk.Grid(column_spacing=12, row_spacing=6, margin=6)
        self.add(self.grid)

    def _add_field(self, row, col, label_text, value, change_cb, obj):
        lbl = Gtk.Label(label=label_text + ":", xalign=1)
        self.grid.attach(lbl, col, row, 1, 1)

        entry = Gtk.Entry()
        # Convert None to empty string for display
        entry.set_text(str(value) if value is not None else "")
        entry.set_hexpand(True)
        entry.connect("changed", change_cb, obj)
        self.grid.attach(entry, col + 1, row, 1, 1)

        if id(obj) not in self._widgets:
            self._widgets[id(obj)] = {}
        self._widgets[id(obj)][label_text] = entry

    def _add_bool_field(self, row, col, label_text, value, change_cb, obj):
        lbl = Gtk.Label(label=label_text + ":", xalign=1)
        self.grid.attach(lbl, col, row, 1, 1)

        check = Gtk.CheckButton()
        check.set_active(value)
        check.connect("toggled", change_cb, obj)
        self.grid.attach(check, col + 1, row, 1, 1)

        if id(obj) not in self._widgets:
            self._widgets[id(obj)] = {}
        self._widgets[id(obj)][label_text] = check

    def _add_multiline_field(self, row, col, label_text, text, change_cb, obj):
        lbl = Gtk.Label(label=label_text + ":", xalign=1, yalign=0)
        self.grid.attach(lbl, col, row, 1, 1)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(180)
        scrolled.set_hexpand(True)

        if HAS_SOURCEVIEW:
            source_view = GtkSource.View()
            source_view.set_show_line_numbers(True)
            source_view.set_auto_indent(True)
            source_view.set_indent_width(4)
            source_view.set_insert_spaces_instead_of_tabs(True)
            source_view.set_tab_width(4)
            font_desc = Pango.FontDescription("monospace 11")
            source_view.override_font(font_desc)

            lang_manager = GtkSource.LanguageManager()
            python_lang = lang_manager.get_language("python")
            if python_lang:
                buffer = source_view.get_buffer()
                buffer.set_language(python_lang)
                buffer.set_highlight_syntax(True)

            buffer = source_view.get_buffer()
            buffer.set_text(text if text else "")
            buffer.connect("changed", change_cb, obj)

            scrolled.add(source_view)

            if id(obj) not in self._widgets:
                self._widgets[id(obj)] = {}
            self._widgets[id(obj)][label_text] = source_view
        else:
            textview = Gtk.TextView()
            textview.set_wrap_mode(Gtk.WrapMode.WORD)
            textview.set_monospace(True)
            textview.get_buffer().set_text(text if text else "")
            textview.get_buffer().connect("changed", change_cb, obj)
            scrolled.add(textview)

            if id(obj) not in self._widgets:
                self._widgets[id(obj)] = {}
            self._widgets[id(obj)][label_text] = textview

        self.grid.attach(scrolled, col + 1, row, 1, 1)
    
    def emit_property_changed(self, obj):
        self.emit('property-changed', obj)

    def emit_property_changed_obj(self, old, obj):
        self.emit('property-changed-obj', (old, obj))