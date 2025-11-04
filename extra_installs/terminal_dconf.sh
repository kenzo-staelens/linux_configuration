#/usr/bin/bash

CONFIG_ROOT=$(git rev-parse --show-toplevel)

dconf load /org/gnome/terminal/legacy/profiles:/:b1dcc9dd-5262-4d8d-a863-c897e6d979b9/ < "$CONFIG_ROOT/extra_installs/terminal_dconf.ini"
