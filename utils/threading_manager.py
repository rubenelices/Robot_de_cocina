"""
Gestor de hilos para ejecución concurrente
Permite ejecutar procesos sin bloquear la interfaz
"""
import threading
from typing import Callable, Optional

class ThreadingManager:
    """
    Gestor de hilos para ejecutar tareas en segundo plano
    
    Mantiene referencia al hilo actual y proporciona métodos
    para iniciar y verificar el estado de las ejecuciones.
    """
    
    def __init__(self):
        """Inicializa el gestor sin hilos activos"""
        self._hilo_actual: Optional[threading.Thread] = None
        self._lock = threading.Lock()
    
    def ejecutar_en_hilo(self, funcion: Callable, *args, **kwargs) -> threading.Thread:
        """
        Ejecuta una función en un hilo separado
        
        Args:
            funcion: Función a ejecutar
            *args: Argumentos posicionales para la función
            **kwargs: Argumentos nombrados para la función
        
        Returns:
            Referencia al hilo creado
        """
        with self._lock:
            # Crear nuevo hilo
            hilo = threading.Thread(
                target=funcion,
                args=args,
                kwargs=kwargs,
                daemon=True
            )
            
            # Guardar referencia
            self._hilo_actual = hilo
            
            # Iniciar el hilo
            hilo.start()
            
            return hilo
    
    def hay_hilo_activo(self) -> bool:
        """
        Verifica si hay un hilo activo ejecutándose
        
        Returns:
            True si hay un hilo vivo, False en caso contrario
        """
        with self._lock:
            return self._hilo_actual is not None and self._hilo_actual.is_alive()
    
    def esperar_hilo_actual(self, timeout: Optional[float] = None):
        """
        Espera a que termine el hilo actual
        
        Args:
            timeout: Tiempo máximo de espera en segundos (None = sin límite)
        """
        with self._lock:
            hilo = self._hilo_actual
        
        if hilo is not None and hilo.is_alive():
            hilo.join(timeout=timeout)
    
    def obtener_hilo_actual(self) -> Optional[threading.Thread]:
        """
        Obtiene el hilo actual
        
        Returns:
            Referencia al hilo actual o None
        """
        with self._lock:
            return self._hilo_actual