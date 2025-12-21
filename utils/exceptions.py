"""
Excepciones personalizadas del sistema
"""

class RobotCocinaException(Exception):
    """Excepción base para errores del robot de cocina"""
    pass

class RobotApagadoException(RobotCocinaException):
    """Se lanza cuando se intenta operar con el robot apagado"""
    
    def __init__(self, mensaje: str = "El robot está apagado"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ProcesoInvalidoException(RobotCocinaException):
    """Se lanza cuando un proceso no es válido"""
    
    def __init__(self, mensaje: str = "Proceso inválido"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class RecetaNoEncontradaException(RobotCocinaException):
    """Se lanza cuando no se encuentra una receta"""
    
    def __init__(self, mensaje: str = "Receta no encontrada"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)