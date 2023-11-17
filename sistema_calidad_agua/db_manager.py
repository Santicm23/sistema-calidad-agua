
import json
import time
from typing import Any

import zmq

from .constants import DB_PATH, DB_SOCKET


def write_to_db(data: dict[str, Any]) -> None:
    '''Write data to database.'''

    with open(DB_PATH, 'w') as f:
        json.dump(data, f)


def read_from_db() -> dict[str, Any]:
    '''Read data from database.'''

    with open(DB_PATH, 'r') as f:
        return json.load(f)


def write_valid_info(type_sensor: str, value: float, timestamp: float = time.time()) -> None:
    '''Write valid data to database.'''

    if value < 0:
        print(f'Se detectó un error: {value}')
        return

    data = read_from_db()

    data[type_sensor].append({
        'value': value,
        'timestamp': timestamp
    })

    write_to_db(data)


def main() -> None:
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.bind(f'tcp://*:{DB_SOCKET["port"]}')

    while True:
        message = socket.recv_json()

        try:
            assert isinstance(message, dict)

            write_valid_info(message['type_sensor'], message['value'], message['timestamp'])

            socket.send_json({'status': 'ok'})

        except Exception as e:
            print(f'Error: {e}')
            socket.send_json({'status': 'error'})



if __name__ == '__main__':
    main()