
import sys

import zmq

from .constants import monitor_parser, SensorType, PROXY_SOCKET
from .helpers import write_valid_info


def main() -> None:
    args = monitor_parser.parse_args()
    tipo_sensor: SensorType

    try:
        tipo_sensor = SensorType(args.tipo_sensor)
    except ValueError:
        print(f"Tipo de sensor '{args.tipo_sensor}' inválido")
        sys.exit(1)

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(
        f'tcp://{PROXY_SOCKET["host"]}:{PROXY_SOCKET["frontend_port"]}')

    socket.setsockopt(zmq.SUBSCRIBE, bytes(tipo_sensor.value, 'utf-8'))

    while True:
        message = socket.recv_multipart()

        value = float(message[0].decode('utf-8').split()[1])
        
        write_valid_info(tipo_sensor, value)


if __name__ == '__main__':
    main()
