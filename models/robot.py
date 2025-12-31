"""
Modelo del Robot de Cocina
Implementa la lógica central del robot con máquina de estados
"""
from typing import Optional, Callable
from models.proceso import ProcesoCocina
from models.receta import Receta
from utils.exceptions import (
    RobotApagadoException,
    ProcesoInvalidoException
)

# Constantes de estado del robot
ESTADO_APAGADO = "apagado"
ESTADO_ENCENDIDO = "encendido"
ESTADO_EJECUTANDO = "ejecutando"
ESTADO_DETENIDO = "detenido"

class RobotCocina:
    """
    Robot de cocina inteligente con control de estado y ejecución de procesos
    
    Implementa una máquina de estados y encapsulación de atributos internos.
    Permite ejecutar procesos individuales o recetas completas.
    """
    
    def __init__(self):
        """Inicializa el robot en estado apagado"""
        self.__estado = ESTADO_APAGADO
        self.__proceso_actual: Optional[ProcesoCocina] = None
        self.__receta_actual: Optional[Receta] = None
        self.__callback_log: Optional[Callable[[str], None]] = None
        self.__callback_estado: Optional[Callable[[str], None]] = None
        self.__callback_progreso: Optional[Callable[[int, int], None]] = None
    
    # ========== PROPIEDADES (GETTERS) - ENCAPSULACIÓN ==========
    
    @property
    def estado(self) -> str:
        """Obtiene el estado actual del robot"""
        return self.__estado
    
    @property
    def esta_encendido(self) -> bool:
        """Verifica si el robot está encendido"""
        return self.__estado != ESTADO_APAGADO
    
    @property
    def esta_ejecutando(self) -> bool:
        """Verifica si el robot está ejecutando algo"""
        return self.__estado == ESTADO_EJECUTANDO
    
    @property
    def puede_ejecutar(self) -> bool:
        """Verifica si el robot puede ejecutar procesos"""
        return self.__estado in [ESTADO_ENCENDIDO, ESTADO_DETENIDO]
    
    # ========== SETTERS DE CALLBACKS ==========
    
    def set_callback_log(self, callback: Callable[[str], None]):
        """Establece el callback para mensajes de log"""
        self.__callback_log = callback
    
    def set_callback_estado(self, callback: Callable[[str], None]):
        """Establece el callback para cambios de estado"""
        self.__callback_estado = callback
    
    def set_callback_progreso(self, callback: Callable[[int, int], None]):
        """Establece el callback para progreso de receta"""
        self.__callback_progreso = callback
    
    # ========== MÉTODOS PRIVADOS ==========
    
    def __cambiar_estado(self, nuevo_estado: str):
        """
        Cambia el estado interno del robot
        
        Args:
            nuevo_estado: Nuevo estado a establecer
        """
        estado_anterior = self.__estado
        self.__estado = nuevo_estado
        
        self.__log(f"🔄 Estado: {estado_anterior} → {nuevo_estado}")
        
        if self.__callback_estado:
            self.__callback_estado(nuevo_estado)
    
    def __log(self, mensaje: str):
        """
        Envía un mensaje al callback de log
        
        Args:
            mensaje: Mensaje a registrar
        """
        print(f"[ROBOT LOG] {mensaje}")  # Debug en consola
        if self.__callback_log:
            self.__callback_log(mensaje)
    
    def __verificar_encendido(self):
        """
        Verifica que el robot esté encendido
        
        Raises:
            RobotApagadoException: Si el robot está apagado
        """
        if not self.esta_encendido:
            raise RobotApagadoException("El robot debe estar encendido para ejecutar operaciones")
    
    # ========== MÉTODOS PÚBLICOS DE CONTROL ==========
    
    def encender(self):
        """
        Enciende el robot
        
        Solo puede encenderse si está apagado.
        """
        print(f"[ROBOT] encender() llamado. Estado actual: {self.__estado}")
        if self.__estado == ESTADO_APAGADO:
            self.__cambiar_estado(ESTADO_ENCENDIDO)
            self.__log("✅ Robot encendido correctamente")
            self.__log("💡 Sistema listo para recibir instrucciones")
        else:
            self.__log("⚠️ El robot ya está encendido")
    
    def apagar(self):
        """
        Apaga el robot
        
        Si está ejecutando algo, lo detiene primero.
        """
        if self.__estado == ESTADO_APAGADO:
            self.__log("⚠️ El robot ya está apagado")
            return
        
        if self.esta_ejecutando:
            self.__log("⚠️ Deteniendo ejecución antes de apagar...")
            self.parar()
        
        self.__cambiar_estado(ESTADO_APAGADO)
        self.__proceso_actual = None
        self.__receta_actual = None
        self.__log("🔴 Robot apagado")
    
    def parar(self):
        """
        Detiene la ejecución actual
        
        Marca el proceso/receta actual para detención.
        """
        if not self.esta_ejecutando:
            self.__log("⚠️ No hay ninguna ejecución en curso")
            return
        
        self.__log("🛑 Solicitando detención...")
        
        # Detener el proceso actual
        if self.__proceso_actual:
            self.__proceso_actual.detener()
        
        # Detener todos los procesos de la receta actual
        if self.__receta_actual:
            self.__receta_actual.detener_procesos()
        
        self.__cambiar_estado(ESTADO_DETENIDO)
        self.__log("⏸️ Ejecución detenida")
    
    # ========== MÉTODOS DE EJECUCIÓN ==========
    
    def ejecutar_proceso(self, proceso: ProcesoCocina) -> bool:
        """
        Ejecuta un proceso individual
        
        Args:
            proceso: Instancia de ProcesoCocina a ejecutar
        
        Returns:
            True si se completó exitosamente, False si fue detenido
        
        Raises:
            RobotApagadoException: Si el robot está apagado
            ProcesoInvalidoException: Si el proceso no es válido
        """
        self.__verificar_encendido()
        
        if proceso is None:
            raise ProcesoInvalidoException("El proceso no puede ser None")
        
        if not self.puede_ejecutar:
            self.__log("⚠️ El robot no puede ejecutar en su estado actual")
            return False
        
        self.__proceso_actual = proceso
        self.__cambiar_estado(ESTADO_EJECUTANDO)
        
        self.__log(f"\n▶️ Ejecutando: {proceso.get_descripcion()}")
        
        # Ejecutar el proceso
        exito = proceso.ejecutar(self.__log)
        
        self.__proceso_actual = None
        
        if exito:
            self.__cambiar_estado(ESTADO_ENCENDIDO)
            self.__log("✓ Proceso completado\n")
        else:
            self.__cambiar_estado(ESTADO_DETENIDO)
        
        return exito
    
    def ejecutar_receta(self, receta: Receta) -> bool:
        """
        Ejecuta una receta completa
        
        Args:
            receta: Instancia de Receta a ejecutar
        
        Returns:
            True si se completó exitosamente, False si fue detenida
        
        Raises:
            RobotApagadoException: Si el robot está apagado
        """
        self.__verificar_encendido()
        
        if not self.puede_ejecutar:
            self.__log("⚠️ El robot no puede ejecutar en su estado actual")
            return False
        
        self.__receta_actual = receta
        self.__cambiar_estado(ESTADO_EJECUTANDO)
        
        print(f"[ROBOT] Callback progreso configurado: {self.__callback_progreso is not None}")
        
        # Ejecutar la receta
        exito = receta.ejecutar_secuencial(
            callback=self.__log,
            callback_progreso=self.__callback_progreso
        )
        
        self.__receta_actual = None
        
        if exito:
            self.__cambiar_estado(ESTADO_ENCENDIDO)
        else:
            self.__cambiar_estado(ESTADO_DETENIDO)
        
        return exito
    
    def obtener_info(self) -> dict:
        """
        Obtiene información completa del estado del robot
        
        Returns:
            Diccionario con información del robot
        """
        info = {
            'estado': self.__estado,
            'encendido': self.esta_encendido,
            'ejecutando': self.esta_ejecutando,
            'puede_ejecutar': self.puede_ejecutar
        }
        
        if self.__proceso_actual:
            info['proceso_actual'] = self.__proceso_actual.get_descripcion()
        
        if self.__receta_actual:
            info['receta_actual'] = self.__receta_actual.nombre
        
        return info
    
    def __str__(self) -> str:
        """Representación en string del robot"""
        return f"Robot(estado={self.__estado})"
    
    def __repr__(self) -> str:
        return f"RobotCocina(estado='{self.__estado}', encendido={self.esta_encendido})"