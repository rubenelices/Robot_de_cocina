"""
Inicialización de la base de datos con tablas y datos preinstalados (CORREGIDO)
"""
from database.db import DatabaseManager

def inicializar_base_datos():
    """Crea las tablas y carga datos preinstalados si no existen"""
    db = DatabaseManager()
    
    crear_tablas(db)

    # Cargar datos solo si no existen recetas base
    if necesita_datos_iniciales(db):
        cargar_datos_preinstalados(db)


def crear_tablas(db: DatabaseManager):
    """Crea las tablas de la base de datos"""
    schema = """
    CREATE TABLE IF NOT EXISTS recetas_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT
    );

    CREATE TABLE IF NOT EXISTS procesos_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receta_id INTEGER NOT NULL,
        tipo_proceso TEXT NOT NULL,
        parametros TEXT,
        orden INTEGER NOT NULL,
        duracion INTEGER NOT NULL,
        FOREIGN KEY (receta_id) REFERENCES recetas_base(id)
    );

    CREATE TABLE IF NOT EXISTS recetas_usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT
    );

    CREATE TABLE IF NOT EXISTS procesos_usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receta_id INTEGER NOT NULL,
        tipo_proceso TEXT NOT NULL,
        parametros TEXT,
        orden INTEGER NOT NULL,
        duracion INTEGER NOT NULL,
        FOREIGN KEY (receta_id) REFERENCES recetas_usuario(id) ON DELETE CASCADE
    );
    """
    db.ejecutar_script(schema)


def necesita_datos_iniciales(db: DatabaseManager) -> bool:
    """Verifica si necesita cargar datos iniciales"""
    recetas = db.obtener_recetas_base()
    return len(recetas) == 0


def cargar_datos_preinstalados(db: DatabaseManager):
    """Carga recetas preinstaladas en la base de datos usando IDs dinámicos"""

    def insertar_receta(nombre, descripcion, procesos):
        # Insertar la receta y obtener su ID real
        receta_id = db.ejecutar_comando(
            "INSERT INTO recetas_base (nombre, descripcion) VALUES (?, ?)",
            (nombre, descripcion)
        )

        # Insertar procesos asociados
        for orden, (tipo, parametros, duracion) in enumerate(procesos, start=1):
            db.ejecutar_comando(
                """
                INSERT INTO procesos_base 
                (receta_id, tipo_proceso, parametros, orden, duracion)
                VALUES (?, ?, ?, ?, ?)
                """,
                (receta_id, tipo, parametros, orden, duracion)
            )

    # ===========================
    # LISTA DE RECETAS PREINSTALADAS
    # ===========================

    insertar_receta(
        "Gazpacho Andaluz",
        "Sopa fría de tomate típica española",
        [
            ("Trocear", "tomates, pepino, pimiento", 3),
            ("Triturar", "velocidad=alta", 5),
            ("Sofreir", "temperatura=media, tiempo=2min", 2),
        ]
    )

    insertar_receta(
        "Puré de Patatas",
        "Cremoso puré tradicional",
        [
            ("Trocear", "patatas", 2),
            ("Hervir", "temperatura=100C, tiempo=20min", 20),
            ("PrepararPure", "velocidad=media", 3),
        ]
    )

    insertar_receta(
        "Salsa Boloñesa",
        "Salsa italiana de carne",
        [
            ("Picar", "cebolla, ajo", 2),
            ("Sofreir", "temperatura=alta, tiempo=5min", 5),
            ("Triturar", "tomate, velocidad=media", 4),
            ("Hervir", "temperatura=90C, tiempo=30min", 30),
        ]
    )

    insertar_receta(
        "Hummus Casero",
        "Pasta de garbanzos estilo mediterráneo",
        [
            ("Hervir", "garbanzos, temperatura=100C, tiempo=45min", 45),
            ("Triturar", "velocidad=alta", 5),
            ("Picar", "ajo, perejil", 1),
        ]
    )

    insertar_receta(
        "Masa de Pizza",
        "Masa italiana tradicional",
        [
            ("Amasar", "velocidad=baja, tiempo=10min", 10),
            ("Amasar", "velocidad=media, tiempo=5min", 5),
        ]
    )

    insertar_receta(
        "Ensalada de Zanahoria",
        "Zanahoria rallada fresca",
        [
            ("Rallar", "zanahorias, grosor=fino", 2),
            ("Picar", "perejil", 1),
        ]
    )

    insertar_receta(
        "Verduras al Vapor",
        "Cocción saludable de vegetales",
        [
            ("Trocear", "brócoli, zanahoria, calabacín", 3),
            ("Vapor", "temperatura=100C, tiempo=15min", 15),
        ]
    )

    insertar_receta(
        "Sopa de Verduras",
        "Sopa nutritiva casera",
        [
            ("Picar", "cebolla, ajo", 2),
            ("Sofreir", "temperatura=media, tiempo=3min", 3),
            ("Trocear", "verduras variadas", 4),
            ("Hervir", "temperatura=95C, tiempo=25min", 25),
        ]
    )

    insertar_receta(
        "Pesto Genovés",
        "Salsa italiana de albahaca",
        [
            ("Picar", "albahaca, piñones, ajo", 2),
            ("Triturar", "velocidad=alta", 3),
        ]
    )

    insertar_receta(
        "Smoothie Tropical",
        "Batido de frutas frescas",
        [
            ("Trocear", "frutas variadas", 2),
            ("Triturar", "velocidad=alta, tiempo=3min", 3),
        ]
    )

    print("✓ Datos preinstalados cargados correctamente")