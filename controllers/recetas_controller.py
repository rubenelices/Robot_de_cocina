"""
Controlador de Recetas
Gestiona las operaciones CRUD de recetas
"""
from typing import List, Optional
from database.db import DatabaseManager
from models.receta import Receta
from models.procesos_basicos import PROCESOS_DISPONIBLES, _procesos_personalizados_cache
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

            # Establecer favorito (nuevo en v2.0)
            receta.favorito = bool(r_data.get('favorito', 0))

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
    
    def crear_receta_usuario(self, nombre: str, descripcion: str = "") -> Receta:
        """
        Crea una nueva receta de usuario

        Args:
            nombre: Nombre de la receta
            descripcion: Descripción opcional

        Returns:
            Receta creada
        """
        receta_id = self._db.insertar_receta_usuario(nombre, descripcion)

        # Devolver objeto Receta
        receta = Receta(
            id=receta_id,
            nombre=nombre,
            descripcion=descripcion,
            es_base=False
        )

        return receta
    
    def agregar_proceso_a_receta(self, receta_id: int, tipo_proceso: str,
                                parametros: str, duracion: int) -> int:
        """
        Agrega un proceso a una receta de usuario

        Args:
            receta_id: ID de la receta
            tipo_proceso: Tipo del proceso (Picar, Triturar, Batir, etc.)
            parametros: Parámetros del proceso
            duracion: Duración en segundos

        Returns:
            ID del proceso creado

        Raises:
            ValueError: Si el tipo de proceso no existe
        """
        # Verificar si es un proceso básico o personalizado
        if tipo_proceso not in PROCESOS_DISPONIBLES and tipo_proceso not in _procesos_personalizados_cache:
            raise ValueError(f"Tipo de proceso '{tipo_proceso}' no válido")

        # Obtener el siguiente orden
        procesos = self._db.obtener_procesos_receta_usuario(receta_id)
        orden = len(procesos) + 1

        return self._db.insertar_proceso_usuario(
            receta_id, tipo_proceso, parametros, orden, duracion
        )

    def agregar_ingrediente(self, receta_id: int, nombre: str,
                           cantidad: float, unidad: str, orden: int) -> int:
        """
        Agrega un ingrediente a una receta de usuario

        Args:
            receta_id: ID de la receta
            nombre: Nombre del ingrediente
            cantidad: Cantidad numérica
            unidad: Unidad de medida (g, ml, etc.)
            orden: Orden en la lista

        Returns:
            ID del ingrediente creado
        """
        resultado = self._db.ejecutar_comando(
            """
            INSERT INTO ingredientes (receta_id, nombre, cantidad, unidad, orden, es_base)
            VALUES (?, ?, ?, ?, ?, 0)
            """,
            (receta_id, nombre, cantidad, unidad, orden)
        )

        return resultado

    # ========== FAVORITOS (NUEVO v2.0) ==========

    def toggle_favorito(self, receta_id: int, es_base: bool = False) -> bool:
        """
        Alterna el estado de favorito de una receta de usuario

        Args:
            receta_id: ID de la receta
            es_base: Si es receta base (no se permite marcar como favorita)

        Returns:
            Nuevo estado de favorito (True/False)

        Raises:
            ValueError: Si se intenta marcar una receta base como favorita
            RecetaNoEncontradaException: Si no se encuentra la receta
        """
        if es_base:
            raise ValueError("No se pueden marcar recetas preinstaladas como favoritas")

        # Obtener estado actual
        resultado = self._db.ejecutar_query(
            "SELECT favorito FROM recetas_usuario WHERE id = ?",
            (receta_id,)
        )

        if not resultado:
            raise RecetaNoEncontradaException(f"Receta {receta_id} no encontrada")

        # Alternar estado
        nuevo_estado = 0 if resultado[0]['favorito'] else 1

        # Actualizar en BD
        self._db.ejecutar_comando(
            "UPDATE recetas_usuario SET favorito = ? WHERE id = ?",
            (nuevo_estado, receta_id)
        )

        return bool(nuevo_estado)

    def obtener_recetas_favoritas(self) -> List[Receta]:
        """
        Obtiene solo las recetas marcadas como favoritas

        Returns:
            Lista de recetas favoritas
        """
        recetas_data = self._db.ejecutar_query(
            "SELECT * FROM recetas_usuario WHERE favorito = 1 ORDER BY nombre"
        )

        recetas = []
        for r_data in recetas_data:
            receta = Receta(
                id=r_data['id'],
                nombre=r_data['nombre'],
                descripcion=r_data.get('descripcion', ''),
                es_base=False
            )
            receta.favorito = True

            # Cargar procesos
            procesos_data = self._db.obtener_procesos_receta_usuario(r_data['id'])
            receta.cargar_procesos_desde_db(procesos_data)

            recetas.append(receta)

        return recetas

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
        Obtiene la lista de tipos de procesos disponibles (básicos + personalizados)

        Returns:
            Lista de nombres de procesos
        """
        todos = list(PROCESOS_DISPONIBLES.keys())
        todos.extend(_procesos_personalizados_cache.keys())
        return todos
    
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