
import zmq

from sistema_calidad_agua.constants import SYSTEM_SOCKET


def print_title() -> None:
    print('----- Sistema de calidad de agua -----')
    print(f'IP del sistema: {SYSTEM_SOCKET["host"]}')
    print(f'Escuchando información del puerto: {SYSTEM_SOCKET["port"]}')
    print('--------------------------------------\n')


def main() -> None:
    print_title()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.bind(f'tcp://*:{SYSTEM_SOCKET["port"]}')
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        message = socket.recv_multipart()

        print(f"Alerta recibida de {message[0].decode('utf-8')}")
        print(f"Mensaje: '{message[1].decode('utf-8')}'\n")


if __name__ == '__main__':
    main()
