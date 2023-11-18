
import asyncio

import zmq
import zmq.asyncio

from ..constants import HEALTH_CHECK_SOCKET


async def health_check(context: zmq.asyncio.Context) -> None:
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(
        f'tcp://{HEALTH_CHECK_SOCKET["host"]}:{HEALTH_CHECK_SOCKET["port"]}')

    while True:
        await sub_socket.recv()
        sub_socket.send(b'OK')

def auth(context: zmq.asyncio.Context, node_type: str, uuid: str) -> None:
    auth_socket = context.socket(zmq.REQ)
    auth_socket.connect(
        f'tcp://{HEALTH_CHECK_SOCKET["host"]}:{HEALTH_CHECK_SOCKET["port"]}')

    auth_socket.send_json({'id': uuid, 'type': node_type})
    auth_socket.recv()
