"""
Controlador del Robot de Cocina
Capa intermedia entre la UI y el modelo del robot
"""
from models.robot import RobotCocina
from models.receta import Receta
from models.proceso import ProcesoCocina
from utils.threading_manager import ThreadingManager
from utils.exceptions import RobotApagadoException, ProcesoInvalidoException
from typing import Callable, Optional

class RobotController:
    """
    Controlador para gestionar las operaciones del robot
    
    Proporciona una interfaz de alto nivel y maneja la ejecución
    concurrente mediante hilos.
    """
    
    def __init__(self):
        """Inicializa el controlador con un robot y gestor de hilos"""
        self._robot = RobotCocina()
        self._thread_manager = ThreadingManager()
    
    # ========== DELEGACIÓN AL ROBOT ==========
    
    def set_callback_log(self, callback: Callable[[str], None]):
        """Establece el callback de log en el robot"""
        self._robot.set_callback_log(callback)
    
    def set_callback_estado(self, callback: Callable[[str], None]):
        """Establece el callback de estado en el robot"""
        self._robot.set_callback_estado(callback)
    
    def set_callback_progreso(self, callback: Callable[[int, int], None]):
        """Establece el callback de progreso en el robot"""
        self._robot.set_callback_progreso(callback)
    
    @property
    def estado(self) -> str:
        """Obtiene el estado actual del robot"""
        return self._robot.estado
    
    @property
    def esta_encendido(self) -> bool:
        """Verifica si el robot está encendido"""
        return self._robot.esta_encendido
    
    @property
    def esta_ejecutando(self) -> bool:
        """Verifica si el robot está ejecutando"""
        return self._robot.esta_ejecutando
    
    @property
    def robot(self):
        """Expone el robot interno para acceso directo"""
        return self._robot
    
    # ========== OPERACIONES DE CONTROL ==========
    
    def encender(self):
        """Enciende el robot"""
        try:
            self._robot.encender()
            return True
        except Exception as e:
            print(f"Error al encender: {e}")
            return False
    
    def apagar(self):
        """Apaga el robot"""
        try:
            self._robot.apagar()
            return True
        except Exception as e:
            print(f"Error al apagar: {e}")
            return False
    
    def parar(self):
        """Detiene la ejecución actual"""
        try:
            self._robot.parar()
            return True
        except Exception as e:
            print(f"Error al parar: {e}")
            return False

    def ajustar_velocidad(self, nueva_velocidad: int) -> bool:
        """
        Ajusta la velocidad del proceso en ejecución

        Args:
            nueva_velocidad: Nueva velocidad (1-10)

        Returns:
            True si se ajustó correctamente
        """
        try:
            return self._robot.ajustar_velocidad(nueva_velocidad)
        except Exception as e:
            print(f"Error al ajustar velocidad: {e}")
            return False

    def obtener_velocidad_actual(self) -> Optional[int]:
        """Obtiene la velocidad actual del proceso en ejecución"""
        return self._robot.obtener_velocidad_actual()

    # ========== EJECUCIÓN CON HILOS ==========
    
    def ejecutar_proceso_async(self, proceso: ProcesoCocina, 
                              callback_completado: Optional[Callable[[bool], None]] = None):
        """
        Ejecuta un proceso individual en un hilo separado
        
        Args:
            proceso: Proceso a ejecutar
            callback_completado: Función a llamar cuando termine (recibe True/False)
        """
        def wrapper():
            try:
                exito = self._robot.ejecutar_proceso(proceso)
                if callback_completado:
                    callback_completado(exito)
            except RobotApagadoException as e:
                print(f"⚠️ Robot apagado: {e}")
                if callback_completado:
                    callback_completado(False)
            except ProcesoInvalidoException as e:
                print(f"⚠️ Proceso inválido: {e}")
                if callback_completado:
                    callback_completado(False)
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                if callback_completado:
                    callback_completado(False)
        
        self._thread_manager.ejecutar_en_hilo(wrapper)
    
    def ejecutar_receta_async(self, receta: Receta,
                             callback_completado: Optional[Callable[[bool], None]] = None):
        """
        Ejecuta una receta en un hilo separado
        
        Args:
            receta: Receta a ejecutar
            callback_completado: Función a llamar cuando termine
        """
        def wrapper():
            try:
                exito = self._robot.ejecutar_receta(receta)
                if callback_completado:
                    callback_completado(exito)
            except RobotApagadoException as e:
                print(f"⚠️ Robot apagado: {e}")
                if callback_completado:
                    callback_completado(False)
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                if callback_completado:
                    callback_completado(False)
        
        self._thread_manager.ejecutar_en_hilo(wrapper)
    
    def hay_ejecucion_activa(self) -> bool:
        """Verifica si hay una ejecución en curso"""
        return self._thread_manager.hay_hilo_activo()
    
    def obtener_info(self) -> dict:
        """Obtiene información del estado del robot"""
        info = self._robot.obtener_info()
        info['hilo_activo'] = self.hay_ejecucion_activa()
        return info