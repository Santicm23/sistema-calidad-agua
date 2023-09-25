
from enum import Enum


class SensorValues(Enum):
    VALORES_CORRECTOS = 'Valores correctos'
    VALORES_FUERA_RANGO = 'Valores fuera del rango'
    ERRORES = 'Errores'

class SensorType(Enum):
    TEMPERATURA = 'Temperatura'
    PH = 'PH'
    OXIGENO_DISUELTO = 'Oxigeno'
