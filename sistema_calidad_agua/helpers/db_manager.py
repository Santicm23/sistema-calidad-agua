
import json
import time
from typing import Any

from ..constants import SensorType, DB_PATH


def write_to_db(data: dict[str, Any]) -> None:
    '''Write data to database.'''

    with open(DB_PATH, 'w') as f:
        json.dump(data, f)


def read_from_db() -> dict[str, Any]:
    '''Read data from database.'''

    with open(DB_PATH, 'r') as f:
        return json.load(f)


def write_valid_info(type_sensor: SensorType, value: float, timestamp: float = time.time()) -> None:
    '''Write valid data to database.'''

    if value < 0:
        print(f'Se detectó un error: {value}')
        return

    data = read_from_db()

    data[type_sensor.value].append({
        'value': value,
        'timestamp': timestamp
    })

    write_to_db(data)
