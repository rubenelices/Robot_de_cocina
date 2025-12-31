"""
Módulo de gestión de base de datos SQLite
"""
import sqlite3
import os
from typing import List, Dict, Optional

# Ruta de la base de datos (en el directorio raíz del proyecto)
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'robot_cocina.db')

class DatabaseManager:
    """Gestor de conexiones y operaciones con la base de datos"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def ejecutar_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Ejecuta una query SELECT y retorna resultados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def ejecutar_comando(self, comando: str, params: tuple = ()) -> int:
        """Ejecuta un comando INSERT/UPDATE/DELETE"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(comando, params)
            conn.commit()
            return cursor.lastrowid
    
    def ejecutar_script(self, script: str):
        """Ejecuta un script SQL completo"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(script)
            conn.commit()
    
    # ========== OPERACIONES DE RECETAS ==========
    
    def obtener_recetas_base(self) -> List[Dict]:
        """Obtiene todas las recetas preinstaladas"""
        query = "SELECT * FROM recetas_base ORDER BY nombre"
        return self.ejecutar_query(query)
    
    def obtener_recetas_usuario(self) -> List[Dict]:
        """Obtiene todas las recetas del usuario"""
        query = "SELECT * FROM recetas_usuario ORDER BY nombre"
        return self.ejecutar_query(query)
    
    def obtener_procesos_receta_base(self, receta_id: int) -> List[Dict]:
        """Obtiene los procesos de una receta base"""
        query = """
            SELECT * FROM procesos_base 
            WHERE receta_id = ? 
            ORDER BY orden
        """
        return self.ejecutar_query(query, (receta_id,))
    
    def obtener_procesos_receta_usuario(self, receta_id: int) -> List[Dict]:
        """Obtiene los procesos de una receta de usuario"""
        query = """
            SELECT * FROM procesos_usuario 
            WHERE receta_id = ? 
            ORDER BY orden
        """
        return self.ejecutar_query(query, (receta_id,))
    
    def insertar_receta_usuario(self, nombre: str, descripcion: str = "") -> int:
        """Inserta una nueva receta de usuario"""
        comando = """
            INSERT INTO recetas_usuario (nombre, descripcion) 
            VALUES (?, ?)
        """
        return self.ejecutar_comando(comando, (nombre, descripcion))
    
    def insertar_proceso_usuario(self, receta_id: int, tipo: str, 
                                 parametros: str, orden: int, duracion: int) -> int:
        """Inserta un proceso en una receta de usuario"""
        comando = """
            INSERT INTO procesos_usuario 
            (receta_id, tipo_proceso, parametros, orden, duracion) 
            VALUES (?, ?, ?, ?, ?)
        """
        return self.ejecutar_comando(comando, (receta_id, tipo, parametros, orden, duracion))
    
    def eliminar_recetas_usuario(self):
        """Elimina todas las recetas y procesos del usuario (reinicio de fábrica)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM procesos_usuario")
            cursor.execute("DELETE FROM recetas_usuario")
            conn.commit()
    
    def tabla_existe(self, nombre_tabla: str) -> bool:
        """Verifica si una tabla existe"""
        query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        result = self.ejecutar_query(query, (nombre_tabla,))
        return len(result) > 0