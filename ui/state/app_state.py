"""
Sistema de estado centralizado para la aplicación Thermomix
Mantiene el estado global de la UI y la lógica de negocio
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from models.receta import Receta


@dataclass
class AppState:
    """
    Estado centralizado de la aplicación

    Beneficios:
    - Single source of truth
    - Fácil depuración
    - Consistencia entre componentes
    - Facilita testing
    """

    # === ESTADO DEL ROBOT ===
    robot_encendido: bool = False
    robot_estado: str = "apagado"  # "apagado", "encendido", "ejecutando", "detenido"

    # === ESTADO DE EJECUCIÓN DE RECETA ===
    receta_actual: Optional[Receta] = None
    paso_actual: int = 0
    en_ejecucion: bool = False
    paso_completado: bool = False

    # === PANTALLA DE CELEBRACIÓN ===
    mostrar_celebracion: bool = False
    nombre_receta_completada: str = ""

    # === PROGRESO EN TIEMPO REAL ===
    tiempo_inicio_paso: float = 0.0  # timestamp cuando empezó el paso
    duracion_paso_actual: float = 0.0  # duración total del paso en segundos
    progreso_paso_actual: float = 0.0  # 0-100%
    velocidad_actual: int = 5  # velocidad de ejecución 1-10 (5 es normal)

    # === MODO MANUAL (NUEVA FUNCIONALIDAD) ===
    modo_seleccionado: Optional[str] = None  # "Picar", "Triturar", etc.
    modo_advertido: bool = False  # Track si ya se mostró advertencia de modo diferente

    # === NAVEGACIÓN DE UI ===
    vista_actual: str = "dashboard"  # "dashboard", "browser", "execution", "wizard", "config"
    filtro_recetas: str = "todas"  # "todas", "base", "usuario", "favoritas"
    busqueda_texto: str = ""

    # === TEMA ===
    tema_oscuro: bool = False

    # === ESTADO DEL WIZARD DE CREAR RECETA ===
    wizard_paso: int = 1  # 1, 2, 3
    wizard_nombre: str = ""
    wizard_descripcion: str = ""
    wizard_ingredientes: List[Dict[str, Any]] = field(default_factory=list)
    wizard_procesos: List[Dict[str, Any]] = field(default_factory=list)

    # === MÉTODOS DE UTILIDAD ===

    def reset_wizard(self):
        """Reinicia el wizard a su estado inicial"""
        self.wizard_paso = 1
        self.wizard_nombre = ""
        self.wizard_descripcion = ""
        self.wizard_ingredientes = []
        self.wizard_procesos = []

    def reset_execution(self):
        """Reinicia el estado de ejecución"""
        self.receta_actual = None
        self.paso_actual = 0
        self.en_ejecucion = False
        self.paso_completado = False
        self.modo_seleccionado = None
        self.modo_advertido = False
        self.tiempo_inicio_paso = 0.0
        self.duracion_paso_actual = 0.0
        self.progreso_paso_actual = 0.0
        self.mostrar_celebracion = False
        self.nombre_receta_completada = ""

    def cargar_receta(self, receta: Receta):
        """Carga una receta para ejecutar"""
        self.receta_actual = receta
        self.paso_actual = 0
        self.en_ejecucion = False
        self.paso_completado = False
        self.modo_seleccionado = None
        self.modo_advertido = False
        self.vista_actual = "execution"

    def siguiente_paso(self) -> bool:
        """
        Avanza al siguiente paso

        Returns:
            bool: True si hay más pasos, False si se completó la receta
        """
        if not self.receta_actual:
            return False

        self.paso_actual += 1
        self.paso_completado = False
        self.modo_seleccionado = None
        self.modo_advertido = False

        # Verificar si se completó la receta
        if self.paso_actual >= self.receta_actual.get_num_pasos():
            return False

        return True

    def anterior_paso(self) -> bool:
        """
        Retrocede al paso anterior

        Returns:
            bool: True si se pudo retroceder, False si ya estaba en el primero
        """
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.paso_completado = False
            self.modo_seleccionado = None
            self.modo_advertido = False
            return True
        return False

    def get_proceso_actual(self):
        """Obtiene el proceso del paso actual"""
        if not self.receta_actual or self.paso_actual >= self.receta_actual.get_num_pasos():
            return None
        return self.receta_actual.procesos[self.paso_actual]

    def get_modo_recomendado(self) -> Optional[str]:
        """Obtiene el modo recomendado por la receta para el paso actual"""
        proceso = self.get_proceso_actual()
        if not proceso:
            return None
        # Para procesos personalizados, usar _nombre; para los básicos, el nombre de la clase
        if hasattr(proceso, '_nombre'):
            return proceso._nombre
        return proceso.__class__.__name__

    def is_modo_correcto(self) -> bool:
        """Verifica si el modo seleccionado coincide con el recomendado"""
        if not self.modo_seleccionado:
            return False
        modo_recomendado = self.get_modo_recomendado()
        return self.modo_seleccionado == modo_recomendado

    def puede_ejecutar_paso(self) -> bool:
        """Verifica si se puede ejecutar el paso actual"""
        return (
            self.robot_encendido and
            self.receta_actual is not None and
            self.paso_actual < self.receta_actual.get_num_pasos() and
            self.modo_seleccionado is not None and
            not self.en_ejecucion
        )

    def receta_completada(self) -> bool:
        """Verifica si la receta actual está completada"""
        if not self.receta_actual:
            return False
        return self.paso_actual >= self.receta_actual.get_num_pasos()

    def get_progreso_porcentaje(self) -> float:
        """Calcula el porcentaje de progreso de la receta actual"""
        if not self.receta_actual:
            return 0.0
        total = self.receta_actual.get_num_pasos()
        if total == 0:
            return 0.0
        return min((self.paso_actual / total) * 100, 100.0)

    def __repr__(self) -> str:
        """Representación para debugging"""
        return (
            f"AppState(robot={self.robot_estado}, "
            f"vista={self.vista_actual}, "
            f"receta={self.receta_actual.nombre if self.receta_actual else None}, "
            f"paso={self.paso_actual}, "
            f"modo={self.modo_seleccionado})"
        )


# === INSTANCIA GLOBAL ===
# Singleton del estado de la aplicación
app_state = AppState()


# === FUNCIONES DE UTILIDAD ===

def debug_state():
    """Imprime el estado actual para debugging"""
    print("=" * 60)
    print("ESTADO DE LA APLICACIÓN")
    print("=" * 60)
    print(f"Robot: {app_state.robot_estado.upper()}")
    print(f"Vista: {app_state.vista_actual}")
    print(f"Tema: {'Oscuro' if app_state.tema_oscuro else 'Claro'}")

    if app_state.receta_actual:
        print(f"\nReceta Actual: {app_state.receta_actual.nombre}")
        print(f"Paso: {app_state.paso_actual + 1}/{app_state.receta_actual.get_num_pasos()}")
        print(f"Progreso: {app_state.get_progreso_porcentaje():.1f}%")
        print(f"Modo seleccionado: {app_state.modo_seleccionado or 'Ninguno'}")
        print(f"Modo recomendado: {app_state.get_modo_recomendado() or 'N/A'}")
        print(f"En ejecución: {app_state.en_ejecucion}")
        print(f"Paso completado: {app_state.paso_completado}")
    else:
        print("\nReceta Actual: Ninguna")

    if app_state.wizard_nombre:
        print(f"\nWizard Activo: {app_state.wizard_nombre}")
        print(f"Paso del wizard: {app_state.wizard_paso}/3")
        print(f"Ingredientes: {len(app_state.wizard_ingredientes)}")
        print(f"Procesos: {len(app_state.wizard_procesos)}")

    print("=" * 60)
