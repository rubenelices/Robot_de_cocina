"""
Controlador de Recetas
Gestiona las operaciones CRUD de recetas
"""
from typing import List, Optional
from database.db import DatabaseManager
from models.receta import Receta
from models.procesos_basicos import PROCESOS_DISPONIBLES
from utils.exceptions import RecetaNoEncontradaException

class RecetasController:
    """
    Controlador para gestionar recetas base y de usuario
    
    Proporciona métodos para crear, leer y eliminar recetas,
    así como para gestionar sus procesos.
    """
    
    def __init__(self):
        """Inicializa el controlador con acceso a la base de datos"""
        self._db = DatabaseManager()
    
    # ========== LECTURA DE RECETAS ==========
    
    def obtener_recetas_base(self) -> List[Receta]:
        """
        Obtiene todas las recetas preinstaladas
        
        Returns:
            Lista de recetas base con sus procesos cargados
        """
        recetas_data = self._db.obtener_recetas_base()
        recetas = []
        
        for r_data in recetas_data:
            receta = Receta(
                id=r_data['id'],
                nombre=r_data['nombre'],
                descripcion=r_data.get('descripcion', ''),
                es_base=True
            )
            
            # Cargar procesos
            procesos_data = self._db.obtener_procesos_receta_base(r_data['id'])
            receta.cargar_procesos_desde_db(procesos_data)
            
            recetas.append(receta)
        
        return recetas
    
    def obtener_recetas_usuario(self) -> List[Receta]:
        """
        Obtiene todas las recetas del usuario
        
        Returns:
            Lista de recetas de usuario con sus procesos cargados
        """
        recetas_data = self._db.obtener_recetas_usuario()
        recetas = []
        
        for r_data in recetas_data:
            receta = Receta(
                id=r_data['id'],
                nombre=r_data['nombre'],
                descripcion=r_data.get('descripcion', ''),
                es_base=False
            )
            
            # Cargar procesos
            procesos_data = self._db.obtener_procesos_receta_usuario(r_data['id'])
            receta.cargar_procesos_desde_db(procesos_data)
            
            recetas.append(receta)
        
        return recetas
    
    def obtener_todas_recetas(self) -> tuple[List[Receta], List[Receta]]:
        """
        Obtiene todas las recetas (base y usuario)
        
        Returns:
            Tupla con (recetas_base, recetas_usuario)
        """
        return self.obtener_recetas_base(), self.obtener_recetas_usuario()
    
    def obtener_receta_por_id(self, receta_id: int, es_base: bool) -> Optional[Receta]:
        """
        Busca una receta específica por ID
        
        Args:
            receta_id: ID de la receta
            es_base: True si es receta base, False si es de usuario
        
        Returns:
            Receta encontrada o None
        """
        recetas = self.obtener_recetas_base() if es_base else self.obtener_recetas_usuario()
        
        for receta in recetas:
            if receta.id == receta_id:
                return receta
        
        return None
    
    # ========== CREACIÓN DE RECETAS ==========
    
    def crear_receta_usuario(self, nombre: str, descripcion: str = "") -> int:
        """
        Crea una nueva receta de usuario
        
        Args:
            nombre: Nombre de la receta
            descripcion: Descripción opcional
        
        Returns:
            ID de la receta creada
        """
        return self._db.insertar_receta_usuario(nombre, descripcion)
    
    def agregar_proceso_a_receta(self, receta_id: int, tipo_proceso: str,
                                parametros: str, duracion: int) -> int:
        """
        Agrega un proceso a una receta de usuario
        
        Args:
            receta_id: ID de la receta
            tipo_proceso: Tipo del proceso (Picar, Triturar, etc.)
            parametros: Parámetros del proceso
            duracion: Duración en segundos
        
        Returns:
            ID del proceso creado
        
        Raises:
            ValueError: Si el tipo de proceso no existe
        """
        if tipo_proceso not in PROCESOS_DISPONIBLES:
            raise ValueError(f"Tipo de proceso '{tipo_proceso}' no válido")
        
        # Obtener el siguiente orden
        procesos = self._db.obtener_procesos_receta_usuario(receta_id)
        orden = len(procesos) + 1
        
        return self._db.insertar_proceso_usuario(
            receta_id, tipo_proceso, parametros, orden, duracion
        )
    
    # ========== ELIMINACIÓN ==========
    
    def reiniciar_fabrica(self):
        """
        Elimina todas las recetas y procesos del usuario
        (mantiene las recetas base)
        """
        self._db.eliminar_recetas_usuario()
    
    # ========== UTILIDADES ==========
    
    def obtener_tipos_procesos_disponibles(self) -> List[str]:
        """
        Obtiene la lista de tipos de procesos disponibles
        
        Returns:
            Lista de nombres de procesos
        """
        return list(PROCESOS_DISPONIBLES.keys())
    
    def obtener_info_receta(self, receta: Receta) -> dict:
        """
        Obtiene información detallada de una receta
        
        Args:
            receta: Receta a analizar
        
        Returns:
            Diccionario con información
        """
        return {
            'id': receta.id,
            'nombre': receta.nombre,
            'descripcion': receta.descripcion,
            'tipo': 'BASE' if receta.es_base else 'USUARIO',
            'num_pasos': receta.get_num_pasos(),
            'duracion_total': receta.get_duracion_total(),
            'procesos': [p.get_descripcion() for p in receta.procesos]
        }