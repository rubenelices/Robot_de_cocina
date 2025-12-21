"""
Clase abstracta ProcesoCocina y definición de la interfaz
"""
from abc import ABC, abstractmethod
from typing import Callable, Optional
import time

class ProcesoCocina(ABC):
    """
    Clase abstracta que define la interfaz para todos los procesos de cocina.
    
    Implementa el patrón Template Method para la ejecución de procesos.
    Todas las subclases deben implementar ejecutar() y proporcionar
    información sobre duración y descripción.
    """
    
    def __init__(self, parametros: str = ""):
        """
        Inicializa el proceso de cocina
        
        Args:
            parametros: Parámetros específicos del proceso (ej: "velocidad=alta")
        """
        self._parametros = parametros
        self._completado = False
        self._detenido = False
    
    @abstractmethod
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None):
        """
        Ejecuta el proceso de cocina.
        
        Args:
            callback: Función opcional para enviar mensajes de estado
        """
        pass
    
    @abstractmethod
    def get_duracion(self) -> int:
        """Retorna la duración estimada en segundos"""
        pass
    
    @abstractmethod
    def get_descripcion(self) -> str:
        """Retorna una descripción legible del proceso"""
        pass
    
    @property
    def parametros(self) -> str:
        """Obtiene los parámetros del proceso"""
        return self._parametros
    
    def detener(self):
        """Marca el proceso para detención"""
        self._detenido = True
    
    def esta_detenido(self) -> bool:
        """Verifica si el proceso está detenido"""
        return self._detenido
    
    def esta_completado(self) -> bool:
        """Verifica si el proceso se completó"""
        return self._completado
    
    def marcar_completado(self):
        """Marca el proceso como completado"""
        self._completado = True
    
    def simular_proceso(self, duracion: int, 
                       callback: Optional[Callable[[str], None]] = None,
                       pasos: int = 10):
        """
        Simula la ejecución de un proceso con actualizaciones periódicas
        
        Args:
            duracion: Duración total en segundos
            callback: Función para enviar actualizaciones
            pasos: Número de actualizaciones durante el proceso
        """
        tiempo_por_paso = duracion / pasos
        
        for i in range(pasos):
            if self._detenido:
                if callback:
                    callback("⚠️ Proceso detenido por el usuario")
                return False
            
            time.sleep(tiempo_por_paso)
            
            if callback:
                progreso = ((i + 1) / pasos) * 100
                callback(f"   Progreso: {progreso:.0f}%")
        
        self.marcar_completado()
        return True
    
    def __str__(self) -> str:
        """Representación en string del proceso"""
        return f"{self.get_descripcion()} ({self.get_duracion()}s)"