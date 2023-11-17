
import sys
import time

import zmq

from .helpers import is_in_range

from .constants import monitor_parser, SensorType, PROXY_SOCKET, DB_SOCKET, SYSTEM_SOCKET


def print_title(sensor_type: SensorType) -> None:
    print(f'----- Monitor de calidad de agua: {sensor_type.value} -----')
    print(f'IP del sistema: {SYSTEM_SOCKET["host"]}')
    print(f'Escuchando información del puerto: {SYSTEM_SOCKET["port"]}')
    print('--------------------------------------\n')


def main() -> None:
    args = monitor_parser.parse_args()
    tipo_sensor: SensorType

    try:
        tipo_sensor = SensorType(args.tipo_sensor)
    except ValueError:
        print(f"Tipo de sensor '{args.tipo_sensor}' inválido")
        sys.exit(1)
    
    print_title(tipo_sensor)

    context = zmq.Context()

    #* Comunicación con el proxy de sensores
    socket_sensors = context.socket(zmq.SUB)
    socket_sensors.connect(
        f'tcp://{PROXY_SOCKET["host"]}:{PROXY_SOCKET["frontend_port"]}')
    socket_sensors.setsockopt(zmq.SUBSCRIBE, bytes(tipo_sensor.value, 'utf-8'))

    #* Comunicación con la base de datos
    socket_db = context.socket(zmq.REQ)
    socket_db.connect(
        f'tcp://{DB_SOCKET["host"]}:{DB_SOCKET["port"]}')
    
    #* Comunicación con el sistema
    socket_system = context.socket(zmq.PUB)
    socket_system.connect(
        f'tcp://{SYSTEM_SOCKET["host"]}:{SYSTEM_SOCKET["port"]}')

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

        if response['status'] == 'ok':
            if not is_in_range(tipo_sensor, value):
                socket_system.send_multipart([
                    bytes(tipo_sensor.value, 'utf-8'),
                    bytes(f'Valor fuera de rango: {value}', 'utf-8')
                ])
        else:
            print(f'Error: {response["message"]}')


if __name__ == '__main__':
    main()
