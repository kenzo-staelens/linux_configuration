from .renderer_window_dispatch import CommandListDispatch
from .renderer_window_nav import CommandListNav


class CommandList(CommandListNav, CommandListDispatch):
    ...