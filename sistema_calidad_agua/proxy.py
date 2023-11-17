
import zmq

from .constants import PROXY_SOCKET


def print_title() -> None:
    print('--------- Proxy de sensores ---------')
    print(f'IP del proxy: {PROXY_SOCKET["host"]}')
    print(f'Escuchando información del puerto: {PROXY_SOCKET["backend_port"]}')
    print(f'Publicando información al puerto: {PROXY_SOCKET["frontend_port"]}')
    print('-------------------------------------\n')


def main() -> None:

    context = zmq.Context()

    frontend_socket = context.socket(zmq.XPUB)
    frontend_socket.bind(f'tcp://*:{PROXY_SOCKET["frontend_port"]}')

    backend_socket = context.socket(zmq.XSUB)
    backend_socket.bind(f'tcp://*:{PROXY_SOCKET["backend_port"]}')

    print_title()

    zmq.proxy(frontend_socket, backend_socket)

    frontend_socket.close()
    backend_socket.close()
    context.term()


if __name__ == '__main__':
    main()
