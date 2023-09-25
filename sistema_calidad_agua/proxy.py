
import signal
import zmq

from .constants.net import PROXY_SOCKET

def main() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    context = zmq.Context()

    frontend_socket = context.socket(zmq.XPUB)
    frontend_socket.bind(f'tcp://*:{PROXY_SOCKET["frontend_port"]}')

    backend_socket = context.socket(zmq.XSUB)
    backend_socket.bind(f'tcp://*:{PROXY_SOCKET["backend_port"]}')

    zmq.proxy(frontend_socket, backend_socket)

    frontend_socket.close()
    backend_socket.close()
    context.term()


if __name__ == '__main__':
    main()
