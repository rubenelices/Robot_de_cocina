"""
Componentes comunes y reutilizables de la UI
Incluye: toggle de modo oscuro, separadores, badges, etc.
"""

from nicegui import ui
from ui.state.app_state import app_state
from ui.styles.colors import COLORS


def create_dark_mode_toggle():
    """
    Crea el toggle de modo oscuro (Sol/Luna)

    Returns:
        ui.button: Botón de toggle
    """

    def toggle_dark_mode():
        """Alterna entre modo claro y oscuro"""
        app_state.tema_oscuro = not app_state.tema_oscuro

        # Actualizar DOM con transición suave
        ui.run_javascript(f'''
            const html = document.documentElement;

            // Añadir transición temporal
            html.style.transition = 'background-color 0.3s ease, color 0.3s ease';

            if ({str(app_state.tema_oscuro).lower()}) {{
                html.classList.add('dark');
                localStorage.setItem('thermomix_dark_mode', 'true');
            }} else {{
                html.classList.remove('dark');
                localStorage.setItem('thermomix_dark_mode', 'false');
            }}

            // Remover transición después (previene flashing en updates)
            setTimeout(() => {{
                html.style.transition = '';
            }}, 300);
        ''')

        # Actualizar icono del botón
        btn._props['icon'] = 'dark_mode' if app_state.tema_oscuro else 'light_mode'
        btn.update()

        # Notificación
        msg = '🌙 Modo oscuro activado' if app_state.tema_oscuro else '☀️ Modo claro activado'
        ui.notify(msg, type='info', position='top')

    # Icono inicial basado en estado
    icono_inicial = 'dark_mode' if app_state.tema_oscuro else 'light_mode'

    # Crear botón
    btn = ui.button(icon=icono_inicial, on_click=toggle_dark_mode).props('flat round').classes(
        'text-2xl transition-transform hover:scale-110 active:scale-95 '
        'text-gray-700 dark:text-gray-300 hover:text-thermo-cyan-500 '
        'dark:hover:text-thermo-cyan-400'
    ).style('padding: 0.5rem;')

    btn.tooltip('Alternar modo oscuro/claro')

    return btn


def create_separator(margin: str = '2rem 0', height: str = '2px'):
    """
    Crea un separador horizontal estilizado

    Args:
        margin: Margen CSS (ej: '2rem 0')
        height: Altura del separador

    Returns:
        ui.element: Separador
    """
    return ui.separator().classes(
        'bg-gray-300 dark:bg-gray-700'
    ).style(
        f'height: {height}; margin: {margin};'
    )


def create_badge(text: str, color: str = 'cyan'):
    """
    Crea un badge/pill estilizado

    Args:
        text: Texto del badge
        color: Color del badge ('cyan', 'green', 'red', 'orange', 'gray')

    Returns:
        ui.badge: Badge component
    """
    color_map = {
        'cyan': 'bg-thermo-cyan-500 text-white',
        'green': 'bg-thermo-green text-gray-900',
        'red': 'bg-thermo-red text-white',
        'orange': 'bg-thermo-orange text-white',
        'gray': 'bg-gray-500 text-white',
    }

    badge_class = color_map.get(color, color_map['cyan'])

    return ui.badge(text).classes(
        f'{badge_class} font-semibold px-3 py-1 rounded-full text-sm'
    )


def create_icon_button(icon: str, on_click, tooltip: str = '', color: str = 'gray'):
    """
    Crea un botón circular con icono

    Args:
        icon: Nombre del icono Material
        on_click: Callback al hacer clic
        tooltip: Texto del tooltip (opcional)
        color: Color del botón

    Returns:
        ui.button: Botón con icono
    """
    btn = ui.button(icon=icon, on_click=on_click).props('flat round dense')

    # Aplicar color
    if color == 'cyan':
        btn.classes('text-thermo-cyan-500 hover:text-thermo-cyan-600')
    elif color == 'red':
        btn.classes('text-red-500 hover:text-red-600')
    elif color == 'green':
        btn.classes('text-green-500 hover:text-green-600')
    elif color == 'orange':
        btn.classes('text-orange-500 hover:text-orange-600')
    else:
        btn.classes('text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200')

    if tooltip:
        btn.tooltip(tooltip)

    return btn


def create_loading_spinner(size: str = 'md'):
    """
    Crea un spinner de carga

    Args:
        size: Tamaño ('sm', 'md', 'lg')

    Returns:
        ui.spinner: Spinner animado
    """
    size_map = {
        'sm': '2rem',
        'md': '3rem',
        'lg': '4rem',
    }

    spinner_size = size_map.get(size, size_map['md'])

    return ui.spinner('dots', size=spinner_size, color='#06b6d4')


def create_card_container(title: str = '', with_header: bool = True):
    """
    Crea un contenedor de tarjeta estilizado

    Args:
        title: Título de la tarjeta (opcional)
        with_header: Si debe incluir header

    Returns:
        ui.card: Tarjeta contenedora
    """
    card = ui.card().classes(
        'w-full bg-white dark:bg-gray-800 '
        'rounded-2xl shadow-lg '
        'border border-gray-200 dark:border-gray-700 '
        'p-6'
    )

    if with_header and title:
        with card:
            ui.label(title).classes(
                'text-2xl font-bold '
                'text-thermo-navy-700 dark:text-white '
                'mb-4'
            )

    return card


def create_confirmation_dialog(
    title: str,
    message: str,
    on_confirm,
    on_cancel=None,
    confirm_text: str = 'Confirmar',
    cancel_text: str = 'Cancelar'
):
    """
    Crea un diálogo de confirmación

    Args:
        title: Título del diálogo
        message: Mensaje de confirmación
        on_confirm: Callback al confirmar
        on_cancel: Callback al cancelar (opcional)
        confirm_text: Texto del botón de confirmación
        cancel_text: Texto del botón de cancelación
    """
    with ui.dialog() as dialog:
        with ui.card().classes(
            'bg-white dark:bg-gray-900 p-6 rounded-3xl max-w-md'
        ):
            # Título
            ui.label(title).classes(
                'text-2xl font-bold text-gray-900 dark:text-white mb-4'
            )

            # Mensaje
            ui.label(message).classes(
                'text-base text-gray-700 dark:text-gray-300 mb-6 leading-relaxed'
            )

            # Botones
            with ui.row().classes('w-full justify-end gap-3'):
                ui.button(
                    cancel_text,
                    icon='close',
                    on_click=lambda: [dialog.close(), on_cancel() if on_cancel else None]
                ).props('outline color=gray').classes('px-6 py-2 rounded-xl')

                ui.button(
                    confirm_text,
                    icon='check_circle',
                    on_click=lambda: [dialog.close(), on_confirm()]
                ).props('unelevated').classes(
                    'bg-thermo-cyan-500 hover:bg-thermo-cyan-600 '
                    'text-white px-6 py-2 rounded-xl'
                )

    dialog.open()


def create_glass_card():
    """
    Crea una tarjeta con efecto glass-morphism

    Returns:
        ui.card: Tarjeta con efecto glass
    """
    return ui.card().classes(
        'glass rounded-3xl p-6 '
        'border border-white/20 '
        'shadow-2xl'
    ).style('backdrop-filter: blur(16px);')


def create_led_indicator(color: str, label: str = '', animated: bool = False):
    """
    Crea un indicador LED

    Args:
        color: Color del LED (hex)
        label: Texto junto al LED (opcional)
        animated: Si debe pulsar (para estado ejecutando)

    Returns:
        ui.row: Contenedor con LED y label
    """
    container = ui.row().classes('items-center gap-3')

    with container:
        # LED circular
        led_classes = 'rounded-full'
        if animated:
            led_classes += ' animate-led-pulse'

        ui.element('div').classes(led_classes).style(
            f'width: 30px; height: 30px; '
            f'background: {color}; '
            f'box-shadow: 0 0 25px {color}, inset 0 2px 6px rgba(0,0,0,0.6);'
        )

        # Label (si existe)
        if label:
            ui.label(label).classes(
                'text-lg font-bold '
                'text-gray-900 dark:text-white '
                'uppercase tracking-wide'
            )

    return container


def create_progress_ring(percentage: float, size: str = 'md'):
    """
    Crea un anillo de progreso circular

    Args:
        percentage: Porcentaje de progreso (0-100)
        size: Tamaño ('sm', 'md', 'lg')

    Returns:
        ui.circular_progress: Anillo de progreso
    """
    size_map = {
        'sm': '3rem',
        'md': '5rem',
        'lg': '7rem',
    }

    return ui.circular_progress(
        value=percentage / 100,
        size=size_map.get(size, size_map['md']),
        color='#06b6d4',
        show_value=True
    ).classes('font-bold')


def show_success_notification(message: str):
    """Muestra notificación de éxito"""
    ui.notify(message, type='positive', position='top', timeout=3000)


def show_error_notification(message: str):
    """Muestra notificación de error"""
    ui.notify(message, type='negative', position='top', timeout=5000)


def show_warning_notification(message: str):
    """Muestra notificación de advertencia"""
    ui.notify(message, type='warning', position='top', timeout=4000)


def show_info_notification(message: str):
    """Muestra notificación informativa"""
    ui.notify(message, type='info', position='top', timeout=3000)
