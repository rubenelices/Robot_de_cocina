"""
Robot de Cocina - Aplicación Principal
Punto de entrada del sistema
"""

from nicegui import ui, app
from database.init_db import inicializar_base_datos
from ui.interfaz import crear_interfaz


def main():
    """Función principal que inicializa la aplicación"""
    print("=" * 50)
    print(" ROBOT DE COCINA - SISTEMA DE CONTROL")
    print("=" * 50)
    
    # Inicializar base de datos
    print("\n[1] Inicializando base de datos...")
    inicializar_base_datos()
    print("✓ Base de datos lista")
    
    # Crear interfaz
    print("\n[2] Creando interfaz gráfica...")
    crear_interfaz()
    print("✓ Interfaz creada")

    # Servir archivos estáticos (CSS)
    app.add_static_files('/static', 'ui')
    
    # ⭐ FAVICON PERSONALIZADO THERMOMIX ⭐
    ui.add_head_html('''
        <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%230f172a'/%3E%3Ccircle cx='50' cy='50' r='35' fill='%233b82f6' stroke='%2393c5fd' stroke-width='3'/%3E%3Cpath d='M35 45 L50 35 L65 45 M50 35 L50 65 M40 55 Q50 60 60 55' stroke='%23e2e8f0' stroke-width='4' fill='none' stroke-linecap='round'/%3E%3Ccircle cx='50' cy='70' r='3' fill='%2310b981'/%3E%3C/svg%3E">
    ''')
    
    print("\n[3] Iniciando servidor...")
    print("=" * 50)
    print("🌐 Accede a: http://localhost:8080")
    print("=" * 50)
    
    # Iniciar servidor NiceGUI
    ui.run(
        title="Robot de Cocina",
        port=8080,
        reload=False,
        show=True
    )


if __name__ == "__main__":
    main()