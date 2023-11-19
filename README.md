
# Comandos

## Comandos de configuración:

### Instalar dependencias
```bash
poetry install
```

## Ejecutar nodos:

### Ejecutar sensor
```bash
poetry run sensor -s <tipo-sensor> -t <tiempo-entre-medidas> -c <path-archivo-configuracion>
```

### Ejecutar monitor
```bash
poetry run monitor -s <tipo-sensor>
```

### Ejecutar proxy
```bash
poetry run proxy
```

### Ejecutar db_manager
```bash
poetry run db_manager
```

### Ejecutar health_check
```bash
poetry run health_check
```

### Ejecutar sistema_calidad_agua
```bash
poetry run sistema_calidad_agua
```
