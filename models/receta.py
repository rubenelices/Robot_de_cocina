"""
Modelo de Receta
Representa una receta con su secuencia de procesos
"""
from typing import List, Callable, Optional
from models.proceso import ProcesoCocina
from models.procesos_basicos import crear_proceso

class Receta:
    """
    Representa una receta de cocina con sus pasos ordenados
    
    Una receta es una secuencia de procesos que se ejecutan
    en orden para crear un plato.
    """
    
    def __init__(self, id: int, nombre: str, descripcion: str = "",
                 es_base: bool = False):
        """
        Inicializa una receta

        Args:
            id: Identificador único
            nombre: Nombre de la receta
            descripcion: Descripción opcional
            es_base: Si es una receta preinstalada (True) o de usuario (False)
        """
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._es_base = es_base
        self._procesos: List[ProcesoCocina] = []
        self._favorito = False  # Nuevo en v2.0
    
    @property
    def id(self) -> int:
        """ID de la receta"""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Nombre de la receta"""
        return self._nombre
    
    @property
    def descripcion(self) -> str:
        """Descripción de la receta"""
        return self._descripcion
    
    @property
    def favorito(self) -> bool:
        """Indica si la receta está marcada como favorita"""
        return self._favorito

    @favorito.setter
    def favorito(self, value: bool):
        """Establece el estado de favorito"""
        self._favorito = value

    @property
    def es_base(self) -> bool:
        """Indica si es una receta preinstalada"""
        return self._es_base
    
    @property
    def procesos(self) -> List[ProcesoCocina]:
        """Lista de procesos de la receta"""
        return self._procesos.copy()
    
    def agregar_proceso(self, proceso: ProcesoCocina):
        """
        Agrega un proceso a la receta
        
        Args:
            proceso: Instancia de ProcesoCocina a agregar
        """
        self._procesos.append(proceso)
    
    def cargar_procesos_desde_db(self, procesos_data: List[dict]):
        """
        Carga los procesos desde datos de la base de datos
        
        Args:
            procesos_data: Lista de diccionarios con datos de procesos
        """
        self._procesos.clear()
        
        for proceso_dict in procesos_data:
            tipo = proceso_dict['tipo_proceso']
            parametros = proceso_dict.get('parametros', '')
            duracion = proceso_dict.get('duracion', None)
            
            try:
                proceso = crear_proceso(tipo, parametros, duracion)
                self._procesos.append(proceso)
            except ValueError as e:
                print(f"⚠️ Error cargando proceso: {e}")
    
    def get_duracion_total(self) -> int:
        """
        Calcula la duración total de la receta en segundos
        
        Returns:
            Suma de duraciones de todos los procesos
        """
        return sum(p.get_duracion() for p in self._procesos)
    
    def get_num_pasos(self) -> int:
        """
        Obtiene el número de pasos de la receta
        
        Returns:
            Cantidad de procesos
        """
        return len(self._procesos)
    
    def ejecutar_secuencial(self, callback: Optional[Callable[[str], None]] = None,
                           callback_progreso: Optional[Callable[[int, int], None]] = None) -> bool:
        """
        Ejecuta todos los procesos de la receta secuencialmente
        
        Args:
            callback: Función para enviar mensajes de log
            callback_progreso: Función para actualizar progreso (paso_actual, total_pasos)
        
        Returns:
            True si se completó, False si fue detenido
        """
        total_pasos = len(self._procesos)
        
        if callback:
            callback(f"\n{'='*50}")
            callback(f"🍳 Iniciando receta: {self._nombre}")
            callback(f"{'='*50}")
            callback(f"📋 Pasos totales: {total_pasos}")
            callback(f"⏱️ Duración estimada: {self.get_duracion_total()} segundos")
            callback(f"{'='*50}\n")
        
        for i, proceso in enumerate(self._procesos, 1):
            if callback:
                callback(f"\n--- Paso {i}/{total_pasos} ---")
            
            # Actualizar progreso ANTES de ejecutar el paso
            if callback_progreso:
                print(f"[RECETA] Llamando callback_progreso({i}, {total_pasos})")
                callback_progreso(i, total_pasos)
            
            # Ejecutar el proceso
            exito = proceso.ejecutar(callback)
            
            if not exito:
                if callback:
                    callback(f"\n❌ Receta detenida en paso {i}")
                return False
        
        if callback:
            callback(f"\n{'='*50}")
            callback(f"✅ ¡Receta completada con éxito!")
            callback(f"🍽️ {self._nombre} está lista para servir")
            callback(f"{'='*50}\n")
        
        return True
    
    def detener_procesos(self):
        """Detiene todos los procesos de la receta"""
        for proceso in self._procesos:
            proceso.detener()
    
    def __str__(self) -> str:
        """Representación en string de la receta"""
        tipo = "BASE" if self._es_base else "USUARIO"
        return f"[{tipo}] {self._nombre} - {len(self._procesos)} pasos ({self.get_duracion_total()}s)"
    
    def __repr__(self) -> str:
        return f"Receta(id={self._id}, nombre='{self._nombre}', pasos={len(self._procesos)})"