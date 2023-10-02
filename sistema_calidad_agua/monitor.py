
import zmq

from .constants import monitor_parser, SensorType, PROXY_SOCKET


def main() -> None:
    args = monitor_parser.parse_args()
    tipo_sensor: str

    try:
        tipo_sensor = SensorType(args.tipo_sensor).value
    except ValueError:
        raise ValueError(f"Tipo de sensor '{args.tipo_sensor}' inválido")

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(
        f'tcp://{PROXY_SOCKET["host"]}:{PROXY_SOCKET["frontend_port"]}')

    socket.setsockopt(zmq.SUBSCRIBE, bytes(tipo_sensor, 'utf-8'))

    while True:
        message = socket.recv_multipart()
        print(f'Received: {message}')


if __name__ == '__main__':
    main()
