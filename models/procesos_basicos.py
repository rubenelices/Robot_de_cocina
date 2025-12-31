"""
Implementaciones concretas de procesos de cocina
Cada clase hereda de ProcesoCocina e implementa un proceso específico
"""
from models.proceso import ProcesoCocina
from typing import Callable, Optional

class Picar(ProcesoCocina):
    """Proceso de picado de ingredientes"""
    
    def __init__(self, parametros: str = "ingredientes varios", duracion: int = None):
        super().__init__(parametros)
        self._duracion = duracion if duracion else 2
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"🔪 Iniciando picado: {self._parametros}")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=5)
        
        if exito and callback:
            callback(f"✓ Picado completado: ingredientes finamente cortados")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Picar {self._parametros}"


class Rallar(ProcesoCocina):
    """Proceso de rallado de alimentos"""
    
    def __init__(self, parametros: str = "ingredientes", duracion: int = None):
        super().__init__(parametros)
        self._duracion = duracion if duracion else 2
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"🧀 Iniciando rallado: {self._parametros}")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=5)
        
        if exito and callback:
            callback(f"✓ Rallado completado")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Rallar {self._parametros}"


class Triturar(ProcesoCocina):
    """Proceso de triturado a alta velocidad"""
    
    def __init__(self, parametros: str = "velocidad=media", duracion: int = None):
        super().__init__(parametros)
        # Si se especifica duración, usarla; si no, intentar extraerla de parámetros o usar default
        if duracion:
            self._duracion = duracion
        elif "tiempo=" in parametros:
            try:
                tiempo_str = parametros.split("tiempo=")[1].split(",")[0].replace("min", "")
                self._duracion = int(tiempo_str) * 60
            except:
                self._duracion = 4
        else:
            self._duracion = 4
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        velocidad = "media"
        if "velocidad=" in self._parametros:
            velocidad = self._parametros.split("velocidad=")[1].split(",")[0]
        
        if callback:
            callback(f"⚡ Triturando a velocidad {velocidad}...")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=8)
        
        if exito and callback:
            callback(f"✓ Triturado completado: textura homogénea")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Triturar ({self._parametros})"


class Trocear(ProcesoCocina):
    """Proceso de troceado en cubos o piezas"""
    
    def __init__(self, parametros: str = "ingredientes", duracion: int = None):
        super().__init__(parametros)
        self._duracion = duracion if duracion else 3
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"🔲 Troceando: {self._parametros}")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=6)
        
        if exito and callback:
            callback(f"✓ Troceado completado: piezas uniformes")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Trocear {self._parametros}"


class Amasar(ProcesoCocina):
    """Proceso de amasado para masas y panes"""
    
    def __init__(self, parametros: str = "velocidad=baja", duracion: int = None):
        super().__init__(parametros)
        # Si se especifica duración, usarla; si no, intentar extraerla de parámetros o usar default
        if duracion:
            self._duracion = duracion
        elif "tiempo=" in parametros:
            try:
                tiempo_str = parametros.split("tiempo=")[1].split(",")[0].replace("min", "")
                self._duracion = int(tiempo_str) * 60
            except:
                self._duracion = 10
        else:
            self._duracion = 10
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"🥖 Amasando masa ({self._parametros})...")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=10)
        
        if exito and callback:
            callback(f"✓ Amasado completado: masa lista")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Amasar ({self._parametros})"


class Hervir(ProcesoCocina):
    """Proceso de cocción por ebullición"""
    
    def __init__(self, parametros: str = "temperatura=100C", duracion: int = None):
        super().__init__(parametros)
        # Si se especifica duración, usarla; si no, intentar extraerla de parámetros o usar default
        if duracion:
            self._duracion = duracion
        elif "tiempo=" in parametros:
            try:
                tiempo_str = parametros.split("tiempo=")[1].split(",")[0].replace("min", "")
                self._duracion = int(tiempo_str) * 60
            except:
                self._duracion = 15
        else:
            self._duracion = 15
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        temp = "100°C"
        if "temperatura=" in self._parametros:
            temp = self._parametros.split("temperatura=")[1].split(",")[0]
        
        if callback:
            callback(f"🔥 Hirviendo a {temp}...")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=12)
        
        if exito and callback:
            callback(f"✓ Cocción completada")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Hervir ({self._parametros})"


class Sofreir(ProcesoCocina):
    """Proceso de sofrito con aceite"""
    
    def __init__(self, parametros: str = "temperatura=media", duracion: int = None):
        super().__init__(parametros)
        if duracion:
            self._duracion = duracion
        elif "tiempo=" in parametros:
            try:
                tiempo_str = parametros.split("tiempo=")[1].split(",")[0].replace("min", "")
                self._duracion = int(tiempo_str) * 60
            except:
                self._duracion = 5
        else:
            self._duracion = 5
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"🍳 Sofriendo ingredientes ({self._parametros})...")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=8)
        
        if exito and callback:
            callback(f"✓ Sofrito completado: ingredientes dorados")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Sofreír ({self._parametros})"


class Vapor(ProcesoCocina):
    """Proceso de cocción al vapor"""
    
    def __init__(self, parametros: str = "temperatura=100C", duracion: int = None):
        super().__init__(parametros)
        if duracion:
            self._duracion = duracion
        elif "tiempo=" in parametros:
            try:
                tiempo_str = parametros.split("tiempo=")[1].split(",")[0].replace("min", "")
                self._duracion = int(tiempo_str) * 60
            except:
                self._duracion = 15
        else:
            self._duracion = 15
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"💨 Cocinando al vapor ({self._parametros})...")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=10)
        
        if exito and callback:
            callback(f"✓ Cocción al vapor completada: alimentos tiernos")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Cocinar al vapor ({self._parametros})"


class PrepararPure(ProcesoCocina):
    """Proceso especializado para preparar purés"""
    
    def __init__(self, parametros: str = "velocidad=media", duracion: int = None):
        super().__init__(parametros)
        self._duracion = duracion if duracion else 3
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"🥔 Preparando puré ({self._parametros})...")
        
        exito = self.simular_proceso(self._duracion, callback, pasos=6)
        
        if exito and callback:
            callback(f"✓ Puré listo: textura cremosa perfecta")
        
        return exito
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        return f"Preparar puré ({self._parametros})"


class Pesar(ProcesoCocina):
    """Proceso de pesaje con báscula integrada"""
    
    def __init__(self, parametros: str = "ingrediente=sin especificar", duracion: int = None):
        super().__init__(parametros)
        self._duracion = duracion if duracion else 2
        
        # Extraer peso objetivo de parámetros
        self._peso_objetivo = None
        if "peso=" in parametros:
            try:
                peso_str = parametros.split("peso=")[1].split(",")[0].replace("g", "").replace("kg", "")
                self._peso_objetivo = int(peso_str)
            except:
                self._peso_objetivo = None
    
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        # Extraer nombre del ingrediente
        ingrediente = "ingrediente"
        if "ingrediente=" in self._parametros:
            ingrediente = self._parametros.split("ingrediente=")[1].split(",")[0]
        
        if callback:
            callback(f"⚖️ Iniciando pesaje de {ingrediente}...")
            if self._peso_objetivo:
                callback(f"   Peso objetivo: {self._peso_objetivo}g")
            callback(f"   Calibrando báscula...")
        
        # Simular proceso de pesaje
        import random
        import time
        
        pasos_pesaje = 5
        tiempo_por_paso = self._duracion / pasos_pesaje
        
        for i in range(pasos_pesaje):
            if self._detenido:
                if callback:
                    callback("⚠️ Pesaje detenido por el usuario")
                return False
            
            time.sleep(tiempo_por_paso)
            
            if callback:
                if i == 0:
                    callback("   Tara establecida a 0g")
                elif i < pasos_pesaje - 1:
                    # Simular lectura de peso en progreso
                    if self._peso_objetivo:
                        peso_actual = int(self._peso_objetivo * (i / (pasos_pesaje - 1)))
                        callback(f"   Peso actual: {peso_actual}g / {self._peso_objetivo}g")
                    else:
                        callback(f"   Añadiendo {ingrediente}...")
                else:
                    # Peso final
                    if self._peso_objetivo:
                        peso_final = self._peso_objetivo
                        callback(f"   ✓ Peso alcanzado: {peso_final}g")
                    else:
                        peso_final = random.randint(50, 500)
                        callback(f"   ✓ Peso registrado: {peso_final}g")
        
        self.marcar_completado()
        
        if callback:
            callback(f"✓ Pesaje completado: {ingrediente} medido con precisión")
        
        return True
    
    def get_duracion(self) -> int:
        return self._duracion
    
    def get_descripcion(self) -> str:
        if self._peso_objetivo:
            return f"Pesar ({self._peso_objetivo}g de {self._parametros.split('ingrediente=')[1].split(',')[0] if 'ingrediente=' in self._parametros else 'ingrediente'})"
        return f"Pesar {self._parametros}"


class ProcesoPersonalizado(ProcesoCocina):
    """Clase genérica para procesos personalizados creados por el usuario"""

    def __init__(self, nombre: str, emoji: str, duracion_base: int,
                 parametros: str = "", descripcion: str = ""):
        super().__init__(parametros)
        self._nombre = nombre
        self._emoji = emoji
        self._duracion = duracion_base
        self._descripcion = descripcion

    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        if callback:
            callback(f"{self._emoji} Iniciando {self._nombre}...")

        exito = self.simular_proceso(self._duracion, callback, pasos=8)

        if exito and callback:
            callback(f"✓ {self._nombre} completado")

        return exito

    def get_duracion(self) -> int:
        return self._duracion

    def get_descripcion(self) -> str:
        if self._descripcion:
            return f"{self._nombre}: {self._descripcion}"
        return self._nombre


# Diccionario para mapear nombres a clases (Factory Pattern)
PROCESOS_DISPONIBLES = {
    'Picar': Picar,
    'Rallar': Rallar,
    'Triturar': Triturar,
    'Trocear': Trocear,
    'Amasar': Amasar,
    'Hervir': Hervir,
    'Sofreir': Sofreir,
    'Vapor': Vapor,
    'PrepararPure': PrepararPure,
    'Pesar': Pesar
}

# Cache de procesos personalizados cargados desde BD
_procesos_personalizados_cache = {}

def registrar_proceso_personalizado(nombre: str, emoji: str, duracion_base: int,
                                   parametros_defecto: str = "", descripcion: str = ""):
    """
    Registra un nuevo tipo de proceso personalizado en el sistema

    Args:
        nombre: Nombre único del proceso
        emoji: Emoji representativo
        duracion_base: Duración base en segundos
        parametros_defecto: Parámetros por defecto
        descripcion: Descripción del proceso
    """
    _procesos_personalizados_cache[nombre] = {
        'emoji': emoji,
        'duracion_base': duracion_base,
        'parametros_defecto': parametros_defecto,
        'descripcion': descripcion
    }

def cargar_procesos_personalizados_desde_bd():
    """
    Carga todos los procesos personalizados desde la base de datos

    Debe ser llamado al iniciar la aplicación
    """
    from database.db import DatabaseManager

    db = DatabaseManager()
    procesos = db.obtener_procesos_personalizados()

    for proceso in procesos:
        registrar_proceso_personalizado(
            nombre=proceso['nombre'],
            emoji=proceso['emoji'],
            duracion_base=proceso['duracion_base'],
            parametros_defecto=proceso['parametros_defecto'] or "",
            descripcion=proceso['descripcion'] or ""
        )

def obtener_todos_los_procesos() -> dict:
    """
    Retorna un diccionario con todos los procesos disponibles (básicos + personalizados)

    Returns:
        Dict con nombre del proceso como clave
    """
    todos = PROCESOS_DISPONIBLES.copy()
    for nombre in _procesos_personalizados_cache:
        todos[nombre] = ProcesoPersonalizado
    return todos

def crear_proceso(tipo: str, parametros: str = "", duracion: int = None) -> ProcesoCocina:
    """
    Factory function para crear procesos dinámicamente

    Args:
        tipo: Nombre del tipo de proceso
        parametros: Parámetros del proceso
        duracion: Duración en segundos (opcional)

    Returns:
        Instancia del proceso solicitado

    Raises:
        ValueError: Si el tipo de proceso no existe
    """
    # Primero verificar si es un proceso básico
    if tipo in PROCESOS_DISPONIBLES:
        clase_proceso = PROCESOS_DISPONIBLES[tipo]
        return clase_proceso(parametros, duracion)

    # Luego verificar si es un proceso personalizado
    if tipo in _procesos_personalizados_cache:
        config = _procesos_personalizados_cache[tipo]
        # Usar parámetros proporcionados o los por defecto
        params = parametros if parametros else config['parametros_defecto']
        dur = duracion if duracion else config['duracion_base']

        return ProcesoPersonalizado(
            nombre=tipo,
            emoji=config['emoji'],
            duracion_base=dur,
            parametros=params,
            descripcion=config['descripcion']
        )

    raise ValueError(f"Tipo de proceso '{tipo}' no reconocido")