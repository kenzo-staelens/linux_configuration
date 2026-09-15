from gi.repository import Gtk

class Breadcrumb(Gtk.Box):
    def __init__(self, on_clicked):
        super().__init__(spacing=2)
        self.on_clicked = on_clicked

    def set_path(self, commands):
        # Remove all buttons
        for child in self.get_children():
            self.remove(child)
        if not commands:
            return
        for i, cmd in enumerate(commands):
            if i > 0:
                self.pack_start(Gtk.Label(label=">"), False, False, 0)
            btn = Gtk.Button(label=cmd.name or "(root)")
            btn.connect("clicked", self.on_breadcrumb_btn_clicked, cmd)
            btn.set_relief(Gtk.ReliefStyle.NONE)  # flat look
            self.pack_start(btn, False, False, 0)
        self.show_all()

    def on_breadcrumb_btn_clicked(self, button, command):
        self.on_clicked(command)