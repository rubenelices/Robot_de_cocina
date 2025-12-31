"""
Constantes de colores para la interfaz Thermomix TM6
Mantiene consistencia visual en toda la aplicación
"""

class ThermomixColors:
    """
    Paleta de colores Thermomix TM6 Professional
    Uso: COLORS.PRIMARY, COLORS.ACCENT, etc.
    """

    # === COLORES PRINCIPALES ===
    PRIMARY = '#627d98'  # Navy azul oscuro
    ACCENT = '#06b6d4'  # Cyan brillante
    SUCCESS = '#00ff88'  # Verde éxito
    ERROR = '#ff006e'  # Magenta error
    WARNING = '#ff9500'  # Naranja advertencia
    DANGER = '#ff3b3b'  # Rojo peligro

    # === FONDOS ===
    BG_LIGHT = '#ffffff'
    BG_DARK = '#0d1f2f'
    BG_CARD_LIGHT = '#f9fafb'
    BG_CARD_DARK = '#1f2937'

    # === TEXTOS ===
    TEXT_PRIMARY_LIGHT = '#1f2937'
    TEXT_PRIMARY_DARK = '#f9fafb'
    TEXT_SECONDARY_LIGHT = '#6b7280'
    TEXT_SECONDARY_DARK = '#9ca3af'

    # === ESTADOS LED ===
    LED_OFF = '#ff3b3b'  # Rojo (apagado)
    LED_READY = '#00ff88'  # Verde (listo)
    LED_RUNNING = '#06b6d4'  # Cyan (ejecutando)
    LED_PAUSED = '#ff9500'  # Naranja (pausado)

    # === GRADIENTES (para botones) ===
    GRADIENT_PRIMARY = 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)'
    GRADIENT_SUCCESS = 'linear-gradient(135deg, #00ff88 0%, #00cc66 100%)'
    GRADIENT_DANGER = 'linear-gradient(135deg, #ff3b3b 0%, #ff006e 100%)'
    GRADIENT_WARNING = 'linear-gradient(135deg, #ff9500 0%, #ff7700 100%)'

    # === SOMBRAS CON GLOW ===
    SHADOW_CYAN = '0 0 30px rgba(6, 182, 212, 0.5)'
    SHADOW_GREEN = '0 0 30px rgba(0, 255, 136, 0.5)'
    SHADOW_RED = '0 0 30px rgba(255, 0, 110, 0.5)'
    SHADOW_ORANGE = '0 0 30px rgba(255, 149, 0, 0.5)'


# Instancia global para importación fácil
COLORS = ThermomixColors()


# Mapeo de estados del robot a colores LED
ESTADO_LED_COLORS = {
    'apagado': COLORS.LED_OFF,
    'encendido': COLORS.LED_READY,
    'ejecutando': COLORS.LED_RUNNING,
    'detenido': COLORS.LED_PAUSED,
}


# Iconos de emojis para modos de cocción
MODO_ICONOS = {
    'Picar': '🔪',
    'Rallar': '🧀',
    'Triturar': '⚡',
    'Trocear': '✂️',
    'Amasar': '🥖',
    'Hervir': '🔥',
    'Sofreir': '🍳',
    'Vapor': '💨',
    'PrepararPure': '🥔',
    'Pesar': '⚖️'
}
