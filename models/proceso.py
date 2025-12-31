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
        self._velocidad = 5  # Velocidad por defecto (1-10)
        self._velocidad_modificada = False
    
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

    @property
    def velocidad(self) -> int:
        """Obtiene la velocidad actual del proceso (1-10)"""
        return self._velocidad

    def ajustar_velocidad(self, nueva_velocidad: int):
        """
        Ajusta la velocidad del proceso en tiempo real

        Args:
            nueva_velocidad: Valor entre 1 (muy lento) y 10 (muy rápido)

        Raises:
            ValueError: Si la velocidad está fuera del rango 1-10
        """
        if not 1 <= nueva_velocidad <= 10:
            raise ValueError("La velocidad debe estar entre 1 y 10")

        velocidad_anterior = self._velocidad
        self._velocidad = nueva_velocidad
        self._velocidad_modificada = True
        return velocidad_anterior

    def obtener_factor_velocidad(self) -> float:
        """
        Calcula el factor de tiempo basado en la velocidad

        Returns:
            Factor multiplicador: velocidad 1 = 2x tiempo, velocidad 10 = 0.5x tiempo
        """
        # Velocidad 1 (muy lento): factor 2.0 (el doble de tiempo)
        # Velocidad 5 (normal): factor 1.0 (tiempo normal)
        # Velocidad 10 (muy rápido): factor 0.5 (mitad del tiempo)
        return 2.0 - (self._velocidad - 1) * 0.15

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
            duracion: Duración total en segundos (se ajusta según velocidad)
            callback: Función para enviar actualizaciones
            pasos: Número de actualizaciones durante el proceso
        """
        # Aplicar factor de velocidad
        factor_velocidad = self.obtener_factor_velocidad()
        duracion_ajustada = duracion * factor_velocidad
        tiempo_por_paso = duracion_ajustada / pasos

        velocidad_anterior = self._velocidad

        for i in range(pasos):
            if self._detenido:
                if callback:
                    callback("⚠️ Proceso detenido por el usuario")
                return False

            time.sleep(tiempo_por_paso)

            # Detectar cambio de velocidad y recalcular
            if self._velocidad != velocidad_anterior:
                if callback:
                    callback(f"   ⚡ Velocidad ajustada: {velocidad_anterior} → {self._velocidad}")

                # Recalcular tiempo restante con nueva velocidad
                pasos_restantes = pasos - (i + 1)
                if pasos_restantes > 0:
                    factor_velocidad = self.obtener_factor_velocidad()
                    tiempo_base_restante = (duracion / pasos) * pasos_restantes
                    tiempo_por_paso = (tiempo_base_restante * factor_velocidad) / pasos_restantes

                velocidad_anterior = self._velocidad

            if callback:
                progreso = ((i + 1) / pasos) * 100
                velocidad_info = f" [Vel: {self._velocidad}]" if self._velocidad_modificada else ""
                callback(f"   Progreso: {progreso:.0f}%{velocidad_info}")

        self.marcar_completado()
        return True
    
    def __str__(self) -> str:
        """Representación en string del proceso"""
        return f"{self.get_descripcion()} ({self.get_duracion()}s)"