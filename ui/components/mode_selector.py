"""
Componente de selección de modo de cocción
Permite al usuario elegir entre 10 modos antes de ejecutar cada paso
"""

from nicegui import ui
from ui.state.app_state import app_state
from ui.styles.colors import MODO_ICONOS, COLORS
from typing import Callable, Optional


def create_mode_selector(on_select: Optional[Callable] = None, compact: bool = False):
    """
    Crea el selector de modo de cocción con 10 botones

    Args:
        on_select: Callback function(modo: str) cuando se selecciona un modo
        compact: Si True, usa diseño compacto para espacios reducidos

    Returns:
        ui.column: Contenedor con el selector de modos
    """

    # Lista de todos los modos disponibles
    MODOS_DISPONIBLES = list(MODO_ICONOS.keys())

    def handle_select(modo: str):
        """Maneja la selección de un modo"""
        # Actualizar estado
        app_state.modo_seleccionado = modo

        # Callback externo
        if on_select:
            on_select(modo)

        # Notificación
        ui.notify(f'Modo seleccionado: {modo} {MODO_ICONOS[modo]}', type='info', position='top')

        # Forzar actualización visual
        if container:
            container.update()

    def is_recommended_mode(modo: str) -> bool:
        """Verifica si el modo es el recomendado por la receta"""
        modo_recomendado = app_state.get_modo_recomendado()
        return modo == modo_recomendado if modo_recomendado else False

    def is_selected_mode(modo: str) -> bool:
        """Verifica si el modo está actualmente seleccionado"""
        return app_state.modo_seleccionado == modo

    # Contenedor principal
    container = ui.column().classes('w-full gap-6')

    with container:
        # Título
        if not compact:
            ui.label('Selecciona Modo de Cocción').classes(
                'text-3xl font-bold text-center '
                'text-thermo-navy-700 dark:text-white '
                'tracking-wide'
            )

            # Subtítulo si hay modo recomendado
            modo_recomendado = app_state.get_modo_recomendado()
            if modo_recomendado:
                with ui.row().classes('w-full justify-center items-center gap-2'):
                    ui.icon('lightbulb').classes('text-thermo-cyan-500 text-xl')
                    ui.label(f'Recomendado: {modo_recomendado} {MODO_ICONOS[modo_recomendado]}').classes(
                        'text-sm text-center text-gray-600 dark:text-gray-400 font-medium'
                    )

        # Grid de botones de modo
        grid_classes = (
            'w-full gap-3 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5'
            if not compact else
            'w-full gap-2 grid-cols-5'
        )

        with ui.grid().classes(grid_classes):
            for modo in MODOS_DISPONIBLES:
                create_mode_button(
                    modo=modo,
                    on_click=handle_select,
                    is_recommended=is_recommended_mode(modo),
                    is_selected=is_selected_mode(modo),
                    compact=compact
                )

    return container


def create_mode_button(
    modo: str,
    on_click: Callable,
    is_recommended: bool = False,
    is_selected: bool = False,
    compact: bool = False
):
    """
    Crea un botón individual de modo de cocción

    Args:
        modo: Nombre del modo (ej: "Picar", "Triturar")
        on_click: Callback al hacer clic
        is_recommended: Si es el modo recomendado
        is_selected: Si es el modo actualmente seleccionado
        compact: Modo compacto (botones más pequeños)
    """

    # Clases base del botón
    btn_classes = [
        'relative flex flex-col items-center justify-center',
        'rounded-2xl transition-all duration-300 cursor-pointer',
        'border-2',
    ]

    # Tamaño según modo compact
    if compact:
        btn_classes.append('h-20 p-2')
    else:
        btn_classes.append('h-28 p-4')

    # Fondo
    if is_selected:
        # Modo seleccionado - fondo cyan con brillo
        btn_classes.extend([
            'bg-thermo-cyan-500 dark:bg-thermo-cyan-600',
            'border-thermo-cyan-400',
            'shadow-glow-cyan',
            'scale-105'
        ])
    elif is_recommended:
        # Modo recomendado - borde cyan con ring
        btn_classes.extend([
            'bg-white dark:bg-gray-800',
            'border-thermo-cyan-500',
            'ring-4 ring-thermo-cyan-300 dark:ring-thermo-cyan-700',
            'shadow-glow-cyan',
            'scale-105'
        ])
    else:
        # Modo normal
        btn_classes.extend([
            'bg-white dark:bg-gray-800',
            'border-gray-300 dark:border-gray-600',
            'hover:border-thermo-cyan-400 hover:scale-105',
            'hover:shadow-lg'
        ])

    # Crear botón
    with ui.button(on_click=lambda: on_click(modo)).classes(' '.join(btn_classes)).props('flat'):
        # Icono emoji
        icono_size = 'text-4xl' if not compact else 'text-3xl'
        ui.label(MODO_ICONOS[modo]).classes(f'{icono_size} mb-1')

        # Nombre del modo
        text_color = 'text-white' if is_selected else 'text-gray-800 dark:text-gray-200'
        text_size = 'text-sm' if not compact else 'text-xs'
        ui.label(modo).classes(
            f'{text_size} font-bold {text_color} text-center line-clamp-1'
        )

        # Badge "Recomendado" si aplica
        if is_recommended and not is_selected:
            with ui.element('div').classes(
                'absolute -top-2 -right-2 '
                'bg-thermo-cyan-500 text-white '
                'text-xs font-bold px-2 py-1 rounded-full '
                'shadow-lg'
            ):
                ui.label('✓')


def create_mode_validation_info():
    """
    Muestra información sobre la validación del modo seleccionado
    Aparece debajo del selector de modos
    """

    container = ui.column().classes('w-full gap-2 mt-4')

    with container:
        modo_seleccionado = app_state.modo_seleccionado
        modo_recomendado = app_state.get_modo_recomendado()

        if not modo_seleccionado:
            # Sin modo seleccionado
            with ui.row().classes('items-center gap-2 p-3 rounded-xl bg-gray-100 dark:bg-gray-800'):
                ui.icon('info').classes('text-gray-500 text-xl')
                ui.label('Selecciona un modo para continuar').classes(
                    'text-sm text-gray-600 dark:text-gray-400'
                )

        elif modo_seleccionado == modo_recomendado:
            # Modo correcto
            with ui.row().classes('items-center gap-2 p-3 rounded-xl bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'):
                ui.icon('check_circle').classes('text-green-600 dark:text-green-400 text-xl')
                ui.label(f'Modo correcto: {modo_seleccionado} coincide con la receta').classes(
                    'text-sm text-green-700 dark:text-green-300 font-medium'
                )

        else:
            # Modo diferente - advertencia
            with ui.row().classes('items-center gap-2 p-3 rounded-xl bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800'):
                ui.icon('warning').classes('text-orange-600 dark:text-orange-400 text-xl')
                with ui.column().classes('flex-1 gap-1'):
                    ui.label(f'⚠️ Modo diferente al recomendado').classes(
                        'text-sm text-orange-700 dark:text-orange-300 font-bold'
                    )
                    ui.label(
                        f'Seleccionado: {modo_seleccionado} {MODO_ICONOS[modo_seleccionado]} | '
                        f'Recomendado: {modo_recomendado} {MODO_ICONOS.get(modo_recomendado, "")}'
                    ).classes(
                        'text-xs text-orange-600 dark:text-orange-400'
                    )

    return container


def show_mode_mismatch_dialog(modo_usuario: str, modo_receta: str, on_confirm: Callable):
    """
    Muestra un diálogo de advertencia cuando el modo seleccionado difiere del recomendado

    Args:
        modo_usuario: Modo seleccionado por el usuario
        modo_receta: Modo recomendado por la receta
        on_confirm: Callback si el usuario confirma continuar
    """

    # Verificar compatibilidad
    modos_compatibles = {
        'Picar': ['Trocear', 'Rallar'],
        'Trocear': ['Picar'],
        'Triturar': ['PrepararPure'],
        'PrepararPure': ['Triturar'],
        'Hervir': ['Vapor'],
        'Vapor': ['Hervir'],
    }

    compatibles = modos_compatibles.get(modo_receta, [])
    es_compatible = modo_usuario in compatibles

    with ui.dialog() as dialog:
        with ui.card().classes(
            'bg-white dark:bg-gray-900 p-6 rounded-3xl max-w-lg'
        ):
            # Icono de advertencia
            with ui.row().classes('items-center gap-3 mb-4'):
                icono_color = 'text-orange-500' if es_compatible else 'text-red-500'
                ui.icon('warning').classes(f'text-5xl {icono_color}')
                ui.label('Modo Diferente al Recomendado').classes(
                    'text-2xl font-bold text-gray-900 dark:text-white'
                )

            # Comparación de modos
            with ui.grid().classes('grid-cols-2 gap-4 mb-4'):
                # Modo seleccionado
                with ui.column().classes(
                    'items-center p-4 rounded-xl '
                    'bg-thermo-cyan-50 dark:bg-thermo-cyan-900/20 '
                    'border-2 border-thermo-cyan-300 dark:border-thermo-cyan-700'
                ):
                    ui.label('Tu Selección').classes('text-xs text-gray-600 dark:text-gray-400 mb-2')
                    ui.label(MODO_ICONOS[modo_usuario]).classes('text-5xl mb-1')
                    ui.label(modo_usuario).classes('font-bold text-lg text-gray-900 dark:text-white')

                # Modo recomendado
                with ui.column().classes(
                    'items-center p-4 rounded-xl '
                    'bg-green-50 dark:bg-green-900/20 '
                    'border-2 border-green-300 dark:border-green-700'
                ):
                    ui.label('Recomendado').classes('text-xs text-gray-600 dark:text-gray-400 mb-2')
                    ui.label(MODO_ICONOS[modo_receta]).classes('text-5xl mb-1')
                    ui.label(modo_receta).classes('font-bold text-lg text-gray-900 dark:text-white')

            # Mensaje según compatibilidad
            if es_compatible:
                mensaje = (
                    f"ℹ️ Los modos **{modo_usuario}** y **{modo_receta}** son compatibles y "
                    f"deberían producir resultados similares. Puedes continuar con seguridad."
                )
                color_clase = 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800'
            else:
                mensaje = (
                    f"⚠️ **ADVERTENCIA**: El modo **{modo_usuario}** es muy diferente a **{modo_receta}**. "
                    f"Esto puede afectar significativamente el resultado final de la receta. "
                    f"¿Estás seguro de que deseas continuar?"
                )
                color_clase = 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'

            # Mensaje de advertencia
            with ui.element('div').classes(f'p-4 rounded-xl border-2 {color_clase} mb-6'):
                ui.markdown(mensaje).classes('text-sm text-gray-700 dark:text-gray-300')

            # Botones de acción
            with ui.row().classes('w-full justify-end gap-3'):
                ui.button(
                    'Cancelar y Cambiar Modo',
                    icon='arrow_back',
                    on_click=dialog.close
                ).props('outline color=gray').classes('px-6 py-2 rounded-xl')

                btn_color = 'orange' if es_compatible else 'red'
                ui.button(
                    'Continuar de Todos Modos',
                    icon='check_circle',
                    on_click=lambda: [dialog.close(), on_confirm()]
                ).props(f'unelevated color={btn_color}').classes('px-6 py-2 rounded-xl')

    dialog.open()


def get_mode_color(modo: str) -> str:
    """
    Retorna el color asociado a cada modo

    Args:
        modo: Nombre del modo

    Returns:
        str: Color hex
    """
    mode_colors = {
        'Picar': '#3b82f6',      # Azul
        'Rallar': '#eab308',     # Amarillo
        'Triturar': '#8b5cf6',   # Púrpura
        'Trocear': '#06b6d4',    # Cyan
        'Amasar': '#f59e0b',     # Ámbar
        'Hervir': '#ef4444',     # Rojo
        'Sofreir': '#f97316',    # Naranja
        'Vapor': '#10b981',      # Verde
        'PrepararPure': '#84cc16', # Lima
        'Pesar': '#6b7280',      # Gris
    }
    return mode_colors.get(modo, '#6b7280')
