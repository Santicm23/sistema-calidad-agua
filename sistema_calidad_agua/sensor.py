
import time

import zmq
import signal
from argparse import Namespace

from .constants.parsers import sensor_parser
from .helpers.files import read_config_file
from .constants.values import SensorType, SensorValues
from .helpers.operations import get_sensor_value


def get_args(args: Namespace) -> tuple[str, int, dict[SensorValues, float]]:
    tipo_sensor: str

    try:
        tipo_sensor = SensorType(args.tipo_sensor).value
    except ValueError:
        raise ValueError(f"Tipo de sensor '{args.tipo_sensor}' inválido")

    tiempo: int = args.tiempo
    config = read_config_file(args.config)

    return tipo_sensor, tiempo, config


def main() -> None:
    tipo_sensor, tiempo, config = get_args(sensor_parser.parse_args())

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://*:5555')
    
    while True:
        sensor_value = get_sensor_value(SensorType(tipo_sensor), config)
        socket.send(bytes(f'{tipo_sensor} {sensor_value}', 'utf-8'))
        time.sleep(tiempo)


if __name__ == '__main__':
    main()
