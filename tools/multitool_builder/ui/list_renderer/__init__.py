from .script_list import ScriptListRenderer
from .command_list import CommandListRenderer
from .argument_list import ArgumentListRenderer
from .property_list import PropertyListRenderer

ScriptListRenderer.register()
CommandListRenderer.register()
ArgumentListRenderer.register()
PropertyListRenderer.register()