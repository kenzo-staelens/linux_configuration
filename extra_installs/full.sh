#!/usr/bin/bash

CONFIG_ROOT=$(git rev-parse --show-toplevel)

sh "$CONFIG_ROOT/extra_installs/install_discord.sh"
sh "$CONFIG_ROOT/extra_installs/install_docker.sh"
sh "$CONFIG_ROOT/extra_installs/install_pg_connector.sh"
sh "$CONFIG_ROOT/extra_installs/install_slack.sh"
sh "$CONFIG_ROOT/extra_installs/install_spotx.sh"
sh "$CONFIG_ROOT/extra_installs/set_default_editor.sh"
sh "$CONFIG_ROOT/extra_installs/terminal_dconf.ini"
sh "$CONFIG_ROOT/extra_installs/terminal_dconf.sh"
