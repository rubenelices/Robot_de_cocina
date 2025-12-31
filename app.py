"""
THERMOMIX - Punto de Entrada Principal
Aplicación completa con interfaz modernizada
"""

from nicegui import ui, app
from ui.interfaz import crear_interfaz_principal
from database.init_db import inicializar_base_datos
from ui.state.app_state import app_state

# ===== INICIALIZACIÓN =====
print("Iniciando Thermomix...")

# Inicializar base de datos (incluye migración a v2.0)
inicializar_base_datos()

# ===== CONFIGURACIÓN DE LA APLICACIÓN =====
@ui.page('/')
def main_page():
    """Página principal de la aplicación"""

    # Detectar preferencia de modo oscuro del navegador
    ui.run_javascript('''
        const darkMode = localStorage.getItem('thermomix_dark_mode') === 'true' ||
                        window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (darkMode) {
            document.documentElement.classList.add('dark');
        }
    ''')

    # Crear interfaz principal
    crear_interfaz_principal()


# ===== METADATA DE LA APP =====
# app.add_static_files('/assets', 'assets')  # Deshabilitado - agregar si necesitas assets


if __name__ in {"__main__", "__mp_main__"}:
    print("\n" + "="*60)
    print("  THERMOMIX")
    print("="*60)
    print("\n Características:")
    print("  ✓ Selector de modo manual (10 modos de cocción)")
    print("  ✓ Navegador de recetas con grid responsivo")
    print("  ✓ Wizard de creación de recetas (3 pasos)")
    print("  ✓ Panel de ejecución paso a paso")
    print("  ✓ Sistema de favoritos")
    print("  ✓ Modo oscuro con toggle")
    print("  ✓ Diseño moderno con Tailwind CSS")
    print("  ✓ Interfaz responsive (mobile/tablet/desktop)")
    print("  ✓ Gestión de ingredientes")
    print("\n🌐 Abriendo servidor...")
    print("="*60 + "\n")

    ui.run(
        title='Thermomix NICEGUI',
        port=8080,
        reload=False,  # DESACTIVADO para evitar errores de "client deleted"
        show=True,
        favicon='🍹'  # Icono de batido/licuadora
    )
