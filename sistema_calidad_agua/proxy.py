
import asyncio
import uuid

import zmq
import zmq.asyncio

from .constants import PROXY_SOCKET
from .helpers import health_check, auth


def print_title() -> None:
    print('--------- Proxy de sensores ---------')
    print(f'IP del proxy: {PROXY_SOCKET["host"]}')
    print(f'Escuchando información del puerto: {PROXY_SOCKET["backend_port"]}')
    print(f'Publicando información al puerto: {PROXY_SOCKET["frontend_port"]}')
    print('-------------------------------------\n')


def main() -> None:
    _id = str(uuid.uuid4())

    context = zmq.asyncio.Context()

    auth(context, _id, 'proxy')

    frontend_socket = context.socket(zmq.XPUB)
    frontend_socket.bind(f'tcp://*:{PROXY_SOCKET["frontend_port"]}')

    backend_socket = context.socket(zmq.XSUB)
    backend_socket.bind(f'tcp://*:{PROXY_SOCKET["backend_port"]}')

    print_title()

    asyncio.create_task(health_check(context))

    zmq.proxy(frontend_socket, backend_socket)

    frontend_socket.close()
    backend_socket.close()
    context.term()


if __name__ == '__main__':
    main()
