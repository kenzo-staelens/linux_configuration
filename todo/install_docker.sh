#!/usr/bin/bash

sudo apt install docker.io docker-compose

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
