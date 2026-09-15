from gi.repository import Gtk
from .main_window_components.main_window_dispatch import MainWindowDispatch
from .main_window_components.main_window_nav import MainWindowNav

class MainWindow(MainWindowDispatch, MainWindowNav):
    ...

class Application(Gtk.Application):
    def __init__(self, reconstruct_configs, save_configs=None):
        super().__init__(application_id='com.example.cmdeditor')
        self.reconstruct_configs = reconstruct_configs
        self.save_configs = save_configs

    def do_activate(self):
        win = MainWindow(self.reconstruct_configs, self.save_configs)
        win.set_application(self)
        win.show_all()
