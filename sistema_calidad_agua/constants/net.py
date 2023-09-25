
from typing import TypedDict


Socket = TypedDict('Socket', {
    'host': str,
    'frontend_port': int,
    'backend_port': int,
})

PROXY_SOCKET: Socket = {
    'host': 'localhost', # TODO: Change this to the IP of the proxy server
    'frontend_port': 5555,
    'backend_port': 5556,
}
