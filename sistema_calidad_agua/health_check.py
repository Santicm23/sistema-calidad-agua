
import asyncio

import zmq
import zmq.asyncio

from .constants import HEALTH_CHECK_SOCKET


nodes = []


async def listen_auth(context: zmq.asyncio.Context) -> None:
    socket_auth = context.socket(zmq.REP)

    socket_auth.bind(f'tcp://*:{HEALTH_CHECK_SOCKET["port"]}')

    while True:
        json = socket_auth.recv_json()
        nodes.append(json)
        socket_auth.send(b'OK')


def main() -> None:
    context = zmq.asyncio.Context()

    asyncio.create_task(listen_auth(context))


if __name__ == '__main__':
    main()
