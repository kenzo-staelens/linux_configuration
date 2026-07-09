import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .main_window import MainWindow

class Application(Gtk.Application):
    def __init__(self, reconstruct_configs, save_configs=None):
        super().__init__(application_id='com.example.cmdeditor')
        self.reconstruct_configs = reconstruct_configs
        self.save_configs = save_configs

    def do_activate(self):
        win = MainWindow(self.reconstruct_configs, self.save_configs)
        win.set_application(self)
        win.show_all()
