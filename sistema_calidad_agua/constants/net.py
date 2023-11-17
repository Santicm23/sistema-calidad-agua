
from typing import TypedDict


Socket = TypedDict('Socket', {
    'host': str,
    'port': int,
})

ProxySocket = TypedDict('ProxySocket', {
    'host': str,
    'frontend_port': int,
    'backend_port': int,
})

PROXY_SOCKET: ProxySocket = {
    'host': 'localhost', # TODO: Change this to the IP of the proxy server
    'frontend_port': 5555,
    'backend_port': 5556,
}

SYSTEM_SOCKET: Socket = {
    'host': 'localhost', # TODO: Change this to the IP of the system server
    'port': 5557,
}

DB_SOCKET: Socket = {
    'host': 'localhost', # TODO: Change this to the IP of the database server
    'port': 5558,
}

HEALTH_CHECK_SOCKET: Socket = {
    'host': 'localhost', # TODO: Change this to the IP of the health check server
    'port': 5559,
}
