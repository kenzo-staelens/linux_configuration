import docker
from argparse import Namespace
from typing import Any

def get_docker_ports_in_use():
    cli = docker.DockerClient()

    ports_in_use = set()
    containers = cli.containers.list()

    for container in containers:
        for _, host_ports in container.ports.items():
            if not host_ports:
                continue
            for port in host_ports:
                ports_in_use.add(int(port['HostPort']))

    return ports_in_use


def run(args: Namespace, ctx: dict[str, Any]):
    ports = get_docker_ports_in_use()
    ctx['ports_in_use'] = ports
    if args.port and args.port in ports:
        raise RuntimeError(f'Port {args.port} already in use')
    default_port = 8069
    while default_port in ports:
        default_port += 1
    args.port = default_port