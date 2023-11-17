
import sys
import time

import zmq

from .constants import monitor_parser, SensorType, PROXY_SOCKET, DB_SOCKET


def main() -> None:
    args = monitor_parser.parse_args()
    tipo_sensor: SensorType

    try:
        tipo_sensor = SensorType(args.tipo_sensor)
    except ValueError:
        print(f"Tipo de sensor '{args.tipo_sensor}' inválido")
        sys.exit(1)

    context = zmq.Context()

    socket_sensors = context.socket(zmq.SUB)
    socket_sensors.connect(
        f'tcp://{PROXY_SOCKET["host"]}:{PROXY_SOCKET["frontend_port"]}')
    socket_sensors.setsockopt(zmq.SUBSCRIBE, bytes(tipo_sensor.value, 'utf-8'))

    socket_db = context.socket(zmq.REQ)
    socket_db.connect(
        f'tcp://{DB_SOCKET["host"]}:{DB_SOCKET["port"]}')

    while True:
        message = socket_sensors.recv_multipart()

        value = float(message[0].decode('utf-8').split()[1])

        socket_db.send_json({
            'type_sensor': tipo_sensor.value,
            'value': value,
            'timestamp': time.time()
        })

        response = socket_db.recv_json()

        assert isinstance(response, dict)

        if response['status'] != 'ok':
            print(f'Error: {response["status"]}')


if __name__ == '__main__':
    main()
