
import time
import json

import zmq
import signal
from argparse import Namespace

from .constants.parsers import sensor_parser
from .helpers.files import read_config_file
from .constants.values import SensorType


def get_args(args: Namespace) -> tuple[str, int, dict[str, float]]:
    tipo_sensor: str

    try:
        tipo_sensor = SensorType(args.tipo_sensor).value
    except ValueError:
        raise ValueError(f"Tipo de sensor '{args.tipo_sensor}' inválido")

    tiempo: int = args.tiempo
    config = read_config_file(args.config)

    return tipo_sensor, tiempo, config


def calcular_valor(config: dict[str, float]) -> float:
    return 0.0


def main() -> None:
    tipo_sensor, tiempo, config = get_args(sensor_parser.parse_args())

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://*:5555')

    for _ in range(5):
        socket.send(
            bytes(f'{tipo_sensor} {tiempo} {json.dumps(config)}', 'utf-8'))
        socket.send(b'All is well')
        time.sleep(1)


if __name__ == '__main__':
    main()
