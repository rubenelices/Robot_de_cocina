"""
Configuración y constantes del sistema
"""

# Configuración de la base de datos
DATABASE_PATH = "robot_cocina.db"

# Estados del robot
ESTADO_APAGADO = "apagado"
ESTADO_ENCENDIDO = "encendido"
ESTADO_EJECUTANDO = "ejecutando"
ESTADO_DETENIDO = "detenido"

# Configuración de UI
UI_UPDATE_INTERVAL = 0.1  # segundos
LOG_MAX_LINES = 100

# Colores de estado
COLOR_APAGADO = "red"
COLOR_ENCENDIDO = "green"
COLOR_EJECUTANDO = "blue"
COLOR_DETENIDO = "orange"