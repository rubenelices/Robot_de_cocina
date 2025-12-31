"""
Inicialización de la base de datos con tablas y datos preinstalados (CORREGIDO)
Versión 2.0 - Incluye migración para ingredientes y favoritos
"""
from database.db import DatabaseManager
import sqlite3

def inicializar_base_datos():
    """Crea las tablas y carga datos preinstalados si no existen"""
    db = DatabaseManager()

    crear_tablas(db)

    # NUEVA: Ejecutar migración a v2.0
    migrar_a_v2(db)

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


def migrar_a_v2(db: DatabaseManager):
    """
    Migra la base de datos a la versión 2.0
    Cambios:
    - Tabla ingredientes (con FK a recetas_usuario)
    - Columna favorito en recetas_usuario
    - Columna fecha_creacion en recetas_usuario
    - Tabla procesos_personalizados
    """
    print("\n🔄 Verificando migración a v2.0...")

    print("📦 Migrando base de datos a v2.0...")

    # Paso 1: Crear tabla ingredientes
    try:
        db.ejecutar_script("""
            CREATE TABLE IF NOT EXISTS ingredientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receta_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                cantidad REAL,
                unidad TEXT,
                orden INTEGER NOT NULL,
                es_base BOOLEAN DEFAULT 0,
                FOREIGN KEY (receta_id) REFERENCES recetas_usuario(id) ON DELETE CASCADE
            );
        """)
        print("  ✓ Tabla 'ingredientes' creada")
    except Exception as e:
        print(f"  ⚠ Error al crear tabla ingredientes: {e}")

    # Paso 2: Agregar columna favorito a recetas_usuario
    try:
        db.ejecutar_comando(
            "ALTER TABLE recetas_usuario ADD COLUMN favorito INTEGER DEFAULT 0"
        )
        print("  ✓ Columna 'favorito' agregada a recetas_usuario")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  ℹ Columna 'favorito' ya existe")
        else:
            print(f"  ⚠ Error al agregar columna favorito: {e}")

    # Paso 3: Agregar columna fecha_creacion a recetas_usuario
    # Nota: SQLite no permite DEFAULT CURRENT_TIMESTAMP en ALTER TABLE
    # Usamos NULL como default y lo rellenamos después
    try:
        db.ejecutar_comando(
            "ALTER TABLE recetas_usuario ADD COLUMN fecha_creacion DATETIME"
        )
        print("  ✓ Columna 'fecha_creacion' agregada a recetas_usuario")

        # Rellenar con fecha actual las recetas existentes
        db.ejecutar_comando(
            "UPDATE recetas_usuario SET fecha_creacion = CURRENT_TIMESTAMP WHERE fecha_creacion IS NULL"
        )
        print("  ✓ Fechas actualizadas para recetas existentes")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  ℹ Columna 'fecha_creacion' ya existe")
        else:
            print(f"  ⚠ Error al agregar columna fecha_creacion: {e}")

    # Paso 4: Crear tabla de preferencias de usuario (opcional pero útil)
    try:
        db.ejecutar_script("""
            CREATE TABLE IF NOT EXISTS preferencias_usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clave TEXT NOT NULL UNIQUE,
                valor TEXT
            );
        """)
        print("  ✓ Tabla 'preferencias_usuario' creada")
    except Exception as e:
        print(f"  ⚠ Error al crear tabla preferencias: {e}")

    # Paso 5: Crear tabla de procesos personalizados
    try:
        db.ejecutar_script("""
            CREATE TABLE IF NOT EXISTS procesos_personalizados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                emoji TEXT DEFAULT '⚙️',
                duracion_base INTEGER NOT NULL,
                parametros_defecto TEXT,
                descripcion TEXT,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                activo INTEGER DEFAULT 1
            );
        """)
        print("  ✓ Tabla 'procesos_personalizados' creada")
    except Exception as e:
        print(f"  ⚠ Error al crear tabla procesos_personalizados: {e}")

    print("✅ Migración a v2.0 completada exitosamente\n")

    # Paso 6: Cargar procesos personalizados de ejemplo (solo si la tabla está vacía)
    try:
        procesos = db.ejecutar_query("SELECT COUNT(*) as count FROM procesos_personalizados")
        if procesos[0]['count'] == 0:
            cargar_procesos_ejemplo(db)
    except Exception as e:
        print(f"  ⚠ Error al verificar procesos de ejemplo: {e}")


def cargar_procesos_ejemplo(db: DatabaseManager):
    """Carga algunos procesos personalizados de ejemplo"""
    print("📦 Cargando procesos personalizados de ejemplo...")

    procesos_ejemplo = [
        ("Batir", "🥄", 8, "velocidad=alta", "Batir ingredientes hasta obtener una mezcla homogénea"),
        ("Emulsionar", "💧", 6, "velocidad=media", "Mezclar líquidos inmiscibles formando una emulsión"),
        ("Fermentar", "🌡️", 3600, "temperatura=28C", "Dejar reposar la masa para que fermente"),
        ("Montar", "🍰", 10, "velocidad=alta", "Montar claras o nata hasta punto de nieve"),
        ("Infusionar", "☕", 300, "temperatura=80C", "Extraer sabores mediante infusión en líquido caliente"),
    ]

    for nombre, emoji, duracion, parametros, descripcion in procesos_ejemplo:
        try:
            db.ejecutar_comando(
                """
                INSERT INTO procesos_personalizados
                (nombre, emoji, duracion_base, parametros_defecto, descripcion)
                VALUES (?, ?, ?, ?, ?)
                """,
                (nombre, emoji, duracion, parametros, descripcion)
            )
        except Exception as e:
            print(f"  ⚠ Error al insertar proceso '{nombre}': {e}")

    print("  ✓ Procesos de ejemplo cargados\n")


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