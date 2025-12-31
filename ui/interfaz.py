"""
THERMOMIX - Interfaz Principal
Diseño premium tipo Thermomix real con todas las funcionalidades
"""

from nicegui import ui, app
from controllers.robot_controller import RobotController
from controllers.recetas_controller import RecetasController
from ui.state.app_state import app_state
from typing import Optional
import asyncio
import time


# ===== PALETA DE COLORES THERMOMIX =====
class ThermomixColors:
    """Paleta de colores premium tipo Thermomix TM6"""
    BG_PRIMARY = '#0a0e27'
    BG_SECONDARY = '#1a1f3a'
    BG_CARD = '#1e2640'
    BG_LCD = '#0d1117'
    BG_INPUT = '#0d1117'  # Fondo para inputs y elementos interactivos

    CYAN = '#00d9ff'
    MAGENTA = '#ff006e'
    GREEN = '#00ff88'
    ORANGE = '#ff9500'
    PURPLE = '#a855f7'
    RED = '#ef4444'

    LED_OFF = '#ff3b3b'
    LED_READY = '#00ff88'
    LED_RUNNING = '#00d9ff'
    LED_PAUSED = '#ff9500'

    TEXT_PRIMARY = '#ffffff'
    TEXT_SECONDARY = '#a8b2d1'
    TEXT_LCD = '#00d9ff'

    BTN_POWER = 'linear-gradient(135deg, #00ff88 0%, #00d9a0 100%)'
    BTN_STOP = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
    BTN_EXECUTE = 'linear-gradient(135deg, #a855f7 0%, #9333ea 100%)'
    BTN_ACTION = 'linear-gradient(135deg, #00d9ff 0%, #0099ff 100%)'
    BTN_SECONDARY = 'linear-gradient(135deg, #6b7280 0%, #4b5563 100%)'
    BTN_DANGER = 'linear-gradient(135deg, #ff006e 0%, #c9184a 100%)'

    BORDER_PRIMARY = '#2a3f5f'
    BORDER_ACCENT = '#00d9ff'
    SHADOW_GLOW = '0 0 30px rgba(0, 217, 255, 0.4)'
    SHADOW_GLOW_GREEN = '0 0 30px rgba(0, 255, 136, 0.4)'


COLORS = ThermomixColors()


# ===== ESTILOS CSS GLOBALES =====
def get_global_styles() -> str:
    return f'''
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background: {COLORS.BG_PRIMARY};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {COLORS.TEXT_PRIMARY};
            min-height: 100vh;
        }}

        .nicegui-content {{
            display: flex !important;
            justify-content: center !important;
            align-items: flex-start !important;
            min-height: 100vh !important;
            padding: 1rem;
            background: {COLORS.BG_PRIMARY};
        }}

        .thermomix-container {{
            background: linear-gradient(145deg, {COLORS.BG_SECONDARY}, {COLORS.BG_PRIMARY});
            border: 3px solid {COLORS.BORDER_PRIMARY};
            border-radius: 40px;
            padding: 2rem;
            box-shadow: 0 30px 60px rgba(0,0,0,0.7), {COLORS.SHADOW_GLOW};
            max-width: 1200px;
            width: 95vw;
            margin: 1rem auto;
        }}

        .lcd-screen {{
            background: {COLORS.BG_LCD};
            border: 3px solid {COLORS.BORDER_ACCENT};
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: inset 0 4px 12px rgba(0,0,0,0.9), {COLORS.SHADOW_GLOW};
            min-height: 120px;
        }}

        .log-screen {{
            background: {COLORS.BG_LCD};
            border: 2px solid {COLORS.BORDER_PRIMARY};
            border-radius: 16px;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            color: {COLORS.CYAN};
            max-height: 200px;
            overflow-y: auto;
        }}

        .btn-round {{
            border-radius: 50% !important;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .btn-round:hover:not([disabled]) {{
            transform: translateY(-3px) scale(1.05);
            filter: brightness(1.15);
        }}

        .btn-round:active:not([disabled]) {{
            transform: translateY(2px) scale(0.98);
        }}

        /* Bordes de colores para botones */
        .btn-border-cyan {{
            border: 4px solid {COLORS.CYAN} !important;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.5) !important;
        }}

        .btn-border-green {{
            border: 4px solid {COLORS.GREEN} !important;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.5) !important;
        }}

        .btn-border-purple {{
            border: 4px solid {COLORS.PURPLE} !important;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.5) !important;
        }}

        .btn-border-red {{
            border: 4px solid {COLORS.RED} !important;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.5) !important;
        }}

        .btn-border-gray {{
            border: 4px solid #6b7280 !important;
            box-shadow: 0 0 15px rgba(107, 114, 128, 0.3) !important;
        }}

        @keyframes led-pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .menu-card {{
            background: {COLORS.BG_CARD};
            border: 2px solid {COLORS.BORDER_PRIMARY};
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .menu-card:hover {{
            border-color: {COLORS.CYAN};
            box-shadow: {COLORS.SHADOW_GLOW};
            transform: translateY(-4px);
        }}

        .recipe-card {{
            background: {COLORS.BG_CARD};
            border: 2px solid {COLORS.BORDER_PRIMARY};
            border-radius: 16px;
            padding: 1rem;
            transition: all 0.3s ease;
        }}

        .recipe-card:hover {{
            border-color: {COLORS.CYAN};
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        }}

        .mode-btn {{
            background: {COLORS.BG_CARD};
            border: 2px solid {COLORS.BORDER_PRIMARY};
            border-radius: 12px;
            padding: 0.75rem;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .mode-btn:hover {{
            border-color: {COLORS.CYAN};
            background: rgba(0, 217, 255, 0.1);
        }}

        .mode-btn.selected {{
            border-color: {COLORS.CYAN};
            background: rgba(0, 217, 255, 0.2);
            box-shadow: 0 0 15px rgba(0, 217, 255, 0.4);
        }}

        .progress-bar {{
            width: 100%;
            height: 30px;
            background: {COLORS.BG_CARD};
            border-radius: 15px;
            overflow: hidden;
            border: 2px solid {COLORS.BORDER_PRIMARY};
            position: relative;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, {COLORS.CYAN}, {COLORS.GREEN});
            transition: width 0.1s linear;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: bold;
            color: white;
        }}

        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: {COLORS.BG_SECONDARY}; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb {{ background: {COLORS.BORDER_PRIMARY}; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: {COLORS.CYAN}; }}
    </style>
    '''


# ===== CONTROLADORES GLOBALES =====
robot_ctrl = RobotController()
recetas_ctrl = RecetasController()


# ===== VARIABLES DE ESTADO =====
main_content = None
estado_led = None
estado_texto = None
log_container = None
logs = []


# ===== FUNCIÓN PRINCIPAL =====
def crear_interfaz_principal():
    """Crea la interfaz principal estilo Thermomix"""
    global main_content

    ui.add_head_html(get_global_styles())

    # Contenedor principal centrado tipo Thermomix
    with ui.element('div').classes('thermomix-container'):
        # Header con título y LED
        crear_header_thermomix()

        # Contenido principal (dinámico)
        main_content = ui.column().classes('w-full gap-4 mt-4')

        with main_content:
            renderizar_vista_actual()


def crear_header_thermomix():
    """Header estilo Thermomix con LED y título"""
    global estado_led, estado_texto

    with ui.row().classes('w-full items-center justify-between mb-4'):
        # Logo y título
        with ui.row().classes('items-center gap-3'):
            ui.icon('blender').style(f'font-size: 2.5rem; color: {COLORS.CYAN};')
            with ui.column().classes('gap-0'):
                ui.label('THERMOMIX').style(
                    f'font-size: 1.8rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY}; '
                    f'text-shadow: 0 0 10px {COLORS.CYAN};'
                )
                ui.label('Control Inteligente').style(
                    f'font-size: 0.85rem; color: {COLORS.TEXT_SECONDARY};'
                )

        # LED de estado y botón power
        with ui.row().classes('items-center gap-4'):
            # LED
            with ui.row().classes('items-center gap-2'):
                estado_led = ui.element('div')
                actualizar_led()

                estado_texto = ui.label('').style(
                    f'font-size: 1rem; font-weight: bold; color: {COLORS.TEXT_LCD}; '
                    f'text-transform: uppercase; letter-spacing: 2px;'
                )

            # Botón power
            crear_boton_power_header()


def actualizar_led():
    """Actualiza el LED según el estado del robot"""
    global estado_led, estado_texto

    if robot_ctrl.esta_encendido:
        if app_state.en_ejecucion:
            color = COLORS.LED_RUNNING
            texto = 'EJECUTANDO'
            animation = 'animation: led-pulse 1s infinite;'
        else:
            color = COLORS.LED_READY
            texto = 'LISTO'
            animation = ''
    else:
        color = COLORS.LED_OFF
        texto = 'APAGADO'
        animation = ''

    if estado_led:
        estado_led.style(
            f'width: 20px; height: 20px; border-radius: 50%; '
            f'background: {color}; '
            f'box-shadow: 0 0 15px {color}, 0 0 25px {color}; '
            f'{animation}'
        )

    if estado_texto:
        estado_texto.text = texto


def crear_boton_power_header():
    """Botón de encendido/apagado en el header"""
    es_encendido = robot_ctrl.esta_encendido

    if es_encendido:
        btn = ui.button(icon='power_off', on_click=on_apagar).props('round')
        btn.style(
            f'background: {COLORS.BTN_STOP}; color: white; '
            f'width: 50px; height: 50px; font-size: 1.5rem;'
        )
    else:
        btn = ui.button(icon='power_settings_new', on_click=on_encender).props('round')
        btn.style(
            f'background: {COLORS.BTN_POWER}; color: white; '
            f'width: 50px; height: 50px; font-size: 1.5rem;'
        )


def on_encender():
    """Enciende el robot"""
    robot_ctrl.encender()
    app_state.robot_encendido = True
    app_state.robot_estado = 'encendido'
    agregar_log('🟢 Robot encendido')
    ui.notify('Robot encendido', type='positive', position='top')
    # Refrescar la interfaz recargando la página
    ui.navigate.to('/')


def on_apagar():
    """Apaga el robot"""
    robot_ctrl.apagar()
    app_state.robot_encendido = False
    app_state.robot_estado = 'apagado'
    app_state.reset_execution()
    agregar_log('🔴 Robot apagado')
    ui.notify('Robot apagado', type='warning', position='top')
    # Refrescar la interfaz recargando la página
    ui.navigate.to('/')


# ===== NAVEGACIÓN =====
def navegar_a(vista: str):
    """Navega a una vista específica"""
    app_state.vista_actual = vista
    # Refrescar la interfaz recargando la página
    ui.navigate.to('/')


def renderizar_vista_actual():
    """Renderiza la vista según app_state.vista_actual"""
    vista = app_state.vista_actual

    if vista == 'dashboard':
        renderizar_dashboard()
    elif vista == 'browser':
        renderizar_browser()
    elif vista == 'wizard':
        renderizar_wizard()
    elif vista == 'config':
        renderizar_config()
    elif vista == 'procesos_personalizados':
        renderizar_procesos_personalizados()
    elif vista == 'celebracion':
        renderizar_celebracion()
    else:
        renderizar_dashboard()


# ===== SISTEMA DE LOGS =====
def agregar_log(mensaje: str):
    """Agrega un mensaje al log"""
    global logs, log_container
    timestamp = time.strftime('%H:%M:%S')
    logs.append(f'[{timestamp}] {mensaje}')
    if len(logs) > 50:
        logs.pop(0)

    # Actualizar display si existe
    if log_container:
        try:
            log_container.clear()
            with log_container:
                for log in logs[-10:]:
                    ui.label(log).style(f'color: {COLORS.CYAN}; font-size: 0.85rem;')
        except:
            pass  # Ignorar si el container fue eliminado


# ===== VISTA: DASHBOARD (REDISEÑADO - CENTRADO) =====
def renderizar_dashboard():
    """Dashboard principal con layout centrado y simétrico"""
    global log_container

    # Layout centrado verticalmente
    with ui.column().classes('w-full items-center gap-4'):

        # Si hay receta activa, mostrar panel de ejecución
        if app_state.receta_actual:
            renderizar_panel_receta_activa()
        else:
            # Pantalla LCD principal (sin receta)
            with ui.element('div').classes('lcd-screen').style('width: 100%; max-width: 600px; text-align: center;'):
                ui.label('SIN RECETA').style(
                    f'font-size: 1.8rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY};'
                )
                ui.label('Selecciona una receta para comenzar').style(
                    f'font-size: 1rem; color: {COLORS.TEXT_SECONDARY}; margin-top: 0.5rem;'
                )

        # Botones principales (siempre centrados)
        with ui.row().classes('justify-center gap-6 mt-4 flex-wrap'):
            crear_boton_grande(
                icon='menu_book',
                label='RECETAS',
                color=COLORS.BTN_ACTION,
                border_class='btn-border-cyan',
                on_click=lambda: navegar_a('browser'),
                enabled=True
            )

            crear_boton_grande(
                icon='add_circle',
                label='CREAR',
                color=COLORS.BTN_POWER,
                border_class='btn-border-green',
                on_click=lambda: navegar_a('wizard'),
                enabled=True
            )

            crear_boton_grande(
                icon='auto_awesome',
                label='FUNCIONES',
                color=COLORS.BTN_STOP,
                border_class='btn-border-red',
                on_click=lambda: navegar_a('procesos_personalizados'),
                enabled=True
            )

            crear_boton_grande(
                icon='settings',
                label='CONFIG',
                color=COLORS.BTN_SECONDARY,
                border_class='btn-border-gray',
                on_click=lambda: navegar_a('config'),
                enabled=True
            )

        # Panel colapsable de pasos (solo si hay receta activa)
        if app_state.receta_actual:
            crear_panel_lista_pasos()

        # Panel de logs (centrado y más ancho)
        with ui.element('div').classes('log-screen').style('width: 100%; max-width: 800px; margin-top: 1.5rem;'):
            ui.label('📋 REGISTRO DE ACTIVIDAD').style(
                f'font-size: 0.9rem; font-weight: bold; color: {COLORS.ORANGE}; margin-bottom: 0.5rem;'
            )
            log_container = ui.column().classes('w-full gap-1')
            for log in logs[-10:]:
                ui.label(log).style(f'color: {COLORS.CYAN}; font-size: 0.85rem;')


def crear_panel_lista_pasos():
    """Crea un panel colapsable con la lista completa de pasos de la receta"""
    receta = app_state.receta_actual
    if not receta:
        return

    total_pasos = receta.get_num_pasos()
    paso_actual = app_state.paso_actual

    with ui.expansion(
        text='📋 VER TODOS LOS PASOS',
        icon='list_alt'
    ).classes('w-full').style(f'''
        max-width: 800px;
        background: {COLORS.BG_CARD};
        border: 2px solid {COLORS.BORDER_PRIMARY};
        border-radius: 12px;
        margin-top: 1rem;
    ''').props('dense header-class="text-cyan"'):
        # Contenedor de la lista
        with ui.column().classes('w-full gap-2 pa-2'):
            for i, proceso in enumerate(receta.procesos):
                es_actual = i == paso_actual
                es_completado = i < paso_actual

                # Determinar colores según estado
                if es_completado:
                    bg_color = 'rgba(0, 255, 136, 0.15)'
                    border_color = COLORS.GREEN
                    icon_color = COLORS.GREEN
                    icon = '✓'
                    text_color = COLORS.TEXT_SECONDARY
                elif es_actual:
                    bg_color = 'rgba(0, 217, 255, 0.2)'
                    border_color = COLORS.CYAN
                    icon_color = COLORS.CYAN
                    icon = '▶'
                    text_color = COLORS.TEXT_PRIMARY
                else:
                    bg_color = COLORS.BG_INPUT
                    border_color = COLORS.BORDER_PRIMARY
                    icon_color = COLORS.TEXT_SECONDARY
                    icon = f'{i + 1}'
                    text_color = COLORS.TEXT_SECONDARY

                # Fila del paso
                with ui.element('div').style(f'''
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    padding: 0.6rem 1rem;
                    background: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 10px;
                    {"box-shadow: 0 0 10px " + COLORS.CYAN + ";" if es_actual else ""}
                '''):
                    # Número/icono del paso
                    ui.element('div').style(f'''
                        min-width: 32px;
                        height: 32px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background: {border_color};
                        color: {COLORS.BG_PRIMARY if es_completado or es_actual else COLORS.TEXT_PRIMARY};
                        border-radius: 50%;
                        font-weight: bold;
                        font-size: 0.9rem;
                    ''').text = icon

                    # Descripción del paso
                    with ui.column().classes('flex-grow gap-0'):
                        ui.label(proceso.get_descripcion()).style(
                            f'color: {text_color}; font-size: 0.9rem; font-weight: {"bold" if es_actual else "normal"};'
                        )
                        ui.label(f'⏱ {proceso.get_duracion()}s').style(
                            f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.75rem;'
                        )

                    # Badge de estado
                    if es_completado:
                        ui.label('Completado').style(
                            f'color: {COLORS.GREEN}; font-size: 0.7rem; font-weight: bold; '
                            f'background: rgba(0, 255, 136, 0.2); padding: 0.2rem 0.5rem; border-radius: 4px;'
                        )
                    elif es_actual:
                        ui.label('Actual').style(
                            f'color: {COLORS.CYAN}; font-size: 0.7rem; font-weight: bold; '
                            f'background: rgba(0, 217, 255, 0.2); padding: 0.2rem 0.5rem; border-radius: 4px;'
                        )

            # Resumen al final
            ui.element('hr').style(f'border: none; border-top: 1px solid {COLORS.BORDER_PRIMARY}; margin: 0.5rem 0;')
            with ui.row().classes('w-full justify-between'):
                ui.label(f'Total: {total_pasos} pasos').style(
                    f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.8rem;'
                )
                duracion_total = receta.get_duracion_total()
                mins = duracion_total // 60
                secs = duracion_total % 60
                ui.label(f'Duración: {mins}m {secs}s' if mins > 0 else f'Duración: {secs}s').style(
                    f'color: {COLORS.ORANGE}; font-size: 0.8rem; font-weight: bold;'
                )


def renderizar_panel_receta_activa():
    """Panel cuando hay una receta cargada"""
    receta = app_state.receta_actual
    total = receta.get_num_pasos()
    paso_num = app_state.paso_actual + 1

    # Panel principal de la receta
    with ui.element('div').classes('lcd-screen').style('width: 100%; max-width: 700px; text-align: center;'):
        ui.label(receta.nombre).style(
            f'font-size: 1.5rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY}; margin-bottom: 0.5rem;'
        )

        if app_state.paso_actual < total:
            proceso = receta.procesos[app_state.paso_actual]

            ui.label(f'PASO {paso_num} DE {total}').style(
                f'font-size: 1rem; color: {COLORS.CYAN}; font-weight: bold; margin-bottom: 0.5rem;'
            )
            ui.label(proceso.get_descripcion()).style(
                f'font-size: 1.1rem; color: {COLORS.TEXT_SECONDARY}; margin-bottom: 0.5rem;'
            )

            with ui.row().classes('justify-center gap-4'):
                ui.label(f'⏱ {proceso.get_duracion()}s').style(
                    f'font-size: 0.9rem; color: {COLORS.TEXT_SECONDARY};'
                )
                modo_recomendado = proceso._nombre if hasattr(proceso, '_nombre') else proceso.__class__.__name__
                ui.label(f'💡 {modo_recomendado}').style(
                    f'font-size: 0.9rem; color: {COLORS.ORANGE};'
                )

    # Barra de progreso de la receta
    progreso_receta = (app_state.paso_actual / total * 100) if total > 0 else 0
    with ui.element('div').classes('progress-bar').style('width: 100%; max-width: 700px; position: relative; margin-top: 1rem;'):
        ui.element('div').classes('progress-fill').style(f'width: {progreso_receta:.1f}%;')
        ui.label(f'Progreso: {progreso_receta:.1f}%').style(
            'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); '
            'color: white; font-weight: bold; z-index: 10;'
        )

    # Panel de ejecución en tiempo real
    if app_state.en_ejecucion:
        crear_panel_ejecucion_activa()
    elif app_state.paso_actual < total:
        # Selector de modos y botones de control
        if not app_state.paso_completado:
            renderizar_selector_modos()

        # Botones de acción
        with ui.row().classes('justify-center gap-4 mt-4'):
            if app_state.paso_completado:
                crear_boton_grande(
                    icon='arrow_forward',
                    label='SIGUIENTE',
                    color=COLORS.BTN_ACTION,
                    border_class='btn-border-cyan',
                    on_click=siguiente_paso,
                    enabled=True
                )
            else:
                puede_ejecutar = app_state.modo_seleccionado is not None and robot_ctrl.esta_encendido
                crear_boton_grande(
                    icon='play_arrow',
                    label='EJECUTAR',
                    color=COLORS.BTN_EXECUTE if puede_ejecutar else COLORS.BTN_SECONDARY,
                    border_class='btn-border-purple' if puede_ejecutar else 'btn-border-gray',
                    on_click=iniciar_ejecucion_paso,
                    enabled=puede_ejecutar
                )

        # Botón cancelar
        ui.button('✕ Cancelar Receta', on_click=cancelar_receta).props('flat').style(
            f'color: {COLORS.MAGENTA}; margin-top: 1rem;'
        )


def renderizar_selector_modos():
    """Selector de modos de cocción (incluye procesos personalizados)"""
    from models.procesos_basicos import obtener_todos_los_procesos, _procesos_personalizados_cache

    with ui.element('div').classes('lcd-screen').style('width: 100%; max-width: 700px; margin-top: 1rem;'):
        ui.label('SELECCIONA EL MODO:').style(
            f'font-size: 1rem; font-weight: bold; color: {COLORS.CYAN}; margin-bottom: 1rem; text-align: center;'
        )

        # Modos básicos predefinidos
        modos_basicos = ['Picar', 'Rallar', 'Triturar', 'Trocear', 'Amasar', 'Hervir', 'Sofreir', 'Vapor', 'PrepararPure', 'Pesar']
        iconos_basicos = {'Picar': '🔪', 'Rallar': '🧀', 'Triturar': '⚡', 'Trocear': '✂️', 'Amasar': '🥖',
                  'Hervir': '🔥', 'Sofreir': '🍳', 'Vapor': '💨', 'PrepararPure': '🥔', 'Pesar': '⚖️'}

        # Obtener procesos personalizados
        modos_personalizados = list(_procesos_personalizados_cache.keys())

        # Combinar todos los modos
        todos_modos = modos_basicos + modos_personalizados

        proceso_actual = app_state.receta_actual.procesos[app_state.paso_actual]
        modo_recomendado = proceso_actual._nombre if hasattr(proceso_actual, '_nombre') else proceso_actual.__class__.__name__

        with ui.grid(columns=5).classes('w-full gap-2'):
            for modo in todos_modos:
                is_selected = app_state.modo_seleccionado == modo
                is_recommended = modo == modo_recomendado

                # Obtener emoji del modo
                if modo in iconos_basicos:
                    emoji = iconos_basicos[modo]
                elif modo in _procesos_personalizados_cache:
                    emoji = _procesos_personalizados_cache[modo]['emoji']
                else:
                    emoji = '🔧'

                btn_style = f'''
                    background: {COLORS.BG_CARD if not is_selected else "rgba(0, 217, 255, 0.3)"};
                    border: 2px solid {COLORS.CYAN if is_selected or is_recommended else COLORS.BORDER_PRIMARY};
                    border-radius: 12px;
                    padding: 0.5rem;
                    cursor: pointer;
                    {"box-shadow: 0 0 15px rgba(0, 217, 255, 0.5);" if is_selected else ""}
                '''

                with ui.element('div').style(btn_style).on('click', lambda m=modo: seleccionar_modo(m)):
                    with ui.column().classes('items-center gap-1'):
                        ui.label(emoji).style('font-size: 1.5rem;')
                        ui.label(modo).style(f'font-size: 0.65rem; color: {COLORS.TEXT_PRIMARY}; font-weight: bold;')


# ===== VISTA: CELEBRACIÓN =====
def renderizar_celebracion():
    """Pantalla de celebración al completar una receta"""
    with ui.column().classes('w-full items-center gap-6'):
        # Panel principal de celebración
        with ui.element('div').classes('lcd-screen').style(
            f'width: 100%; max-width: 600px; text-align: center; '
            f'border-color: {COLORS.GREEN}; box-shadow: 0 0 30px {COLORS.GREEN};'
        ):
            ui.label('').style('font-size: 4rem; margin-bottom: 1rem;')

            ui.label('¡RECETA COMPLETADA!').style(
                f'font-size: 2rem; font-weight: bold; color: {COLORS.GREEN}; margin-bottom: 0.5rem;'
            )

            ui.label(app_state.nombre_receta_completada).style(
                f'font-size: 1.3rem; color: {COLORS.TEXT_PRIMARY}; margin-bottom: 1rem;'
            )

            ui.label('¡Que aproveche!').style(
                f'font-size: 1.5rem; font-weight: bold; color: {COLORS.ORANGE}; '
                f'font-style: italic;'
            )

            ui.label('').style('font-size: 3rem; margin-top: 1rem;')

        # Botón para volver al menú
        ui.button('VOLVER AL MENÚ', icon='home', on_click=cerrar_celebracion).style(
            f'background: {COLORS.BTN_ACTION}; color: white; padding: 1rem 2rem; '
            f'font-size: 1.1rem; font-weight: bold; border-radius: 12px; margin-top: 1rem;'
        )


def cerrar_celebracion():
    """Cierra la pantalla de celebración y vuelve al dashboard"""
    app_state.mostrar_celebracion = False
    app_state.nombre_receta_completada = ""
    navegar_a('dashboard')


def crear_boton_grande(icon: str, label: str, color: str, border_class: str, on_click, enabled: bool = True):
    """Crea un botón grande estilo Thermomix con borde de color"""
    with ui.column().classes('items-center gap-2'):
        btn = ui.button(icon=icon, on_click=on_click if enabled else None).props('round').classes(f'btn-round {border_class}')
        btn.style(
            f'width: 100px; height: 100px; font-size: 2.5rem; '
            f'background: {color if enabled else COLORS.BTN_SECONDARY}; color: white; '
            f'opacity: {1 if enabled else 0.5};'
        )
        if not enabled:
            btn.props('disable')

        ui.label(label).style(
            f'font-size: 0.85rem; font-weight: bold; color: {COLORS.TEXT_SECONDARY}; '
            f'text-transform: uppercase; letter-spacing: 1px;'
        )


def seleccionar_modo(modo: str):
    """Selecciona un modo de cocción"""
    app_state.modo_seleccionado = modo
    agregar_log(f'🔧 Modo seleccionado: {modo}')
    ui.notify(f'Modo: {modo}', type='info')
    navegar_a('dashboard')


def crear_panel_ejecucion_activa():
    """Crea el panel de ejecución con actualización en tiempo real"""
    proceso = app_state.receta_actual.procesos[app_state.paso_actual]

    # Estado del timer para tracking de velocidad
    timer_state = {
        'progreso_acumulado': 0.0,  # Progreso acumulado (0-100)
        'ultimo_tick': time.time(),
        'velocidad_anterior': app_state.velocidad_actual
    }

    with ui.element('div').classes('lcd-screen').style(
        f'border-color: {COLORS.LED_RUNNING}; box-shadow: 0 0 20px {COLORS.LED_RUNNING};'
    ):
        ui.label('⚡ EJECUTANDO PASO').style(
            f'font-size: 1.2rem; font-weight: bold; color: {COLORS.LED_RUNNING}; '
            f'text-align: center; margin-bottom: 1rem; animation: led-pulse 1s infinite;'
        )

        ui.label(proceso.get_descripcion()).style(
            f'font-size: 1rem; color: {COLORS.TEXT_PRIMARY}; text-align: center; margin-bottom: 1rem;'
        )

        # Barra de progreso del paso actual
        progreso_label = ui.label('0%').style(
            f'font-size: 2rem; font-weight: bold; color: {COLORS.CYAN}; text-align: center;'
        )

        progress_bar_fill = ui.element('div').classes('progress-bar').style('margin: 1rem 0;')
        with progress_bar_fill:
            progress_inner = ui.element('div').classes('progress-fill').style('width: 0%;')

        tiempo_label = ui.label('Tiempo restante: --').style(
            f'font-size: 0.9rem; color: {COLORS.TEXT_SECONDARY}; text-align: center;'
        )

        # Control de velocidad en tiempo real
        with ui.column().classes('w-full items-center mt-3 gap-2'):
            velocidad_label = ui.label(f'Velocidad: {app_state.velocidad_actual}').style(
                f'font-size: 0.9rem; font-weight: bold; color: {COLORS.ORANGE};'
            )

            velocidad_slider = ui.slider(
                min=1,
                max=10,
                value=app_state.velocidad_actual,
                step=1
            ).classes('w-3/4').props('color=orange label-always')

            velocidad_slider.on('update:model-value', lambda e: ajustar_velocidad_proceso(
                e.args, velocidad_label
            ))

            ui.label('1=Muy lento | 5=Normal | 10=Muy rápido').style(
                f'font-size: 0.75rem; color: {COLORS.TEXT_SECONDARY}; text-align: center;'
            )

        # Botón DETENER
        with ui.row().classes('w-full justify-center mt-4'):
            btn_detener = ui.button('DETENER', icon='stop', on_click=detener_ejecucion).style(
                f'background: {COLORS.BTN_STOP}; color: white; padding: 1rem 2rem; '
                f'font-size: 1.1rem; font-weight: bold; border-radius: 12px;'
            )

        # Timer para actualizar el progreso con soporte para cambio de velocidad
        def actualizar_progreso():
            if not app_state.en_ejecucion:
                timer.deactivate()
                return

            ahora = time.time()
            delta = ahora - timer_state['ultimo_tick']
            timer_state['ultimo_tick'] = ahora

            duracion_base = app_state.duracion_paso_actual

            if duracion_base > 0:
                # Calcular factor de velocidad actual
                # Velocidad 1 = 2x tiempo (más lento), Velocidad 5 = 1x, Velocidad 10 = 0.5x (más rápido)
                velocidad = app_state.velocidad_actual
                factor_velocidad = 2.0 - (velocidad - 1) * (1.5 / 9)  # Mapea 1->2.0, 10->0.5

                # El progreso avanza más rápido con mayor velocidad
                # delta_progreso = (tiempo transcurrido / duración ajustada) * 100
                duracion_ajustada = duracion_base * factor_velocidad
                delta_progreso = (delta / duracion_ajustada) * 100

                timer_state['progreso_acumulado'] += delta_progreso
                progreso = min(timer_state['progreso_acumulado'], 100)

                # Calcular tiempo restante estimado con velocidad actual
                progreso_restante = 100 - progreso
                if progreso_restante > 0:
                    restante = (progreso_restante / 100) * duracion_ajustada
                else:
                    restante = 0

                app_state.progreso_paso_actual = progreso

                # Actualizar UI
                progreso_label.text = f'{progreso:.1f}%'
                progress_inner.style(f'width: {progreso:.1f}%;')
                tiempo_label.text = f'Tiempo restante: {restante:.1f}s'

                # Si se completó
                if progreso >= 100:
                    timer.deactivate()
                    app_state.en_ejecucion = False
                    app_state.paso_completado = True
                    agregar_log(f'✅ Paso {app_state.paso_actual + 1} completado')
                    ui.notify('¡Paso completado!', type='positive')
                    ui.navigate.to('/')

        timer = ui.timer(0.1, actualizar_progreso)


def _ejecutar_paso_real():
    """Ejecuta el paso realmente (después de validación)"""
    receta = app_state.receta_actual
    proceso = receta.procesos[app_state.paso_actual]
    duracion = proceso.get_duracion()

    # Configurar estado de ejecución
    app_state.en_ejecucion = True
    app_state.tiempo_inicio_paso = time.time()
    app_state.duracion_paso_actual = duracion
    app_state.progreso_paso_actual = 0
    app_state.velocidad_actual = 5  # Resetear velocidad a normal

    agregar_log(f'▶️ Ejecutando: {proceso.get_descripcion()} ({duracion}s)')
    ui.notify(f'Ejecutando paso {app_state.paso_actual + 1}...', type='info')

    # Recargar página para mostrar panel de ejecución
    ui.navigate.to('/')


def iniciar_ejecucion_paso():
    """Inicia la ejecución de un paso (llamado desde el botón EJECUTAR)"""
    if not app_state.modo_seleccionado:
        ui.notify('Selecciona un modo primero', type='warning')
        return

    if not robot_ctrl.esta_encendido:
        ui.notify('Enciende el robot primero', type='warning')
        return

    receta = app_state.receta_actual
    proceso = receta.procesos[app_state.paso_actual]

    # Obtener el nombre real del modo recomendado
    # Para procesos personalizados, usar _nombre; para los básicos, el nombre de la clase
    if hasattr(proceso, '_nombre'):
        modo_recomendado = proceso._nombre
    else:
        modo_recomendado = proceso.__class__.__name__

    modo_seleccionado = app_state.modo_seleccionado

    # Validar si el modo seleccionado coincide con el recomendado
    if modo_seleccionado != modo_recomendado:
        # Mostrar diálogo de advertencia
        with ui.dialog() as dialog:
            with ui.card().style(
                f'background: {COLORS.BG_CARD}; border: 2px solid {COLORS.ORANGE}; '
                f'border-radius: 16px; padding: 1.5rem; max-width: 400px;'
            ):
                ui.label('⚠️ Modo diferente al recomendado').style(
                    f'color: {COLORS.ORANGE}; font-size: 1.3rem; font-weight: bold; '
                    f'text-align: center; margin-bottom: 1rem;'
                )

                ui.label(f'Has seleccionado: {modo_seleccionado}').style(
                    f'color: {COLORS.TEXT_PRIMARY}; font-size: 1rem; text-align: center;'
                )
                ui.label(f'La receta recomienda: {modo_recomendado}').style(
                    f'color: {COLORS.CYAN}; font-size: 1rem; text-align: center; margin-bottom: 1rem;'
                )

                ui.label('Usar un modo diferente puede afectar el resultado de la receta.').style(
                    f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.9rem; text-align: center; margin-bottom: 1rem;'
                )

                with ui.row().classes('w-full justify-center gap-3'):
                    ui.button('Cancelar', on_click=dialog.close).style(
                        f'background: {COLORS.BTN_SECONDARY}; color: white; '
                        f'padding: 0.5rem 1.5rem; border-radius: 8px;'
                    )
                    ui.button('Continuar', on_click=lambda: [dialog.close(), _ejecutar_paso_real()]).style(
                        f'background: {COLORS.BTN_STOP}; color: white; '
                        f'padding: 0.5rem 1.5rem; border-radius: 8px;'
                    )
        dialog.open()
    else:
        # Modo correcto, ejecutar directamente
        _ejecutar_paso_real()


def detener_ejecucion():
    """Detiene la ejecución actual"""
    progreso_actual = app_state.progreso_paso_actual
    app_state.en_ejecucion = False
    app_state.tiempo_inicio_paso = 0
    app_state.duracion_paso_actual = 0
    agregar_log(f'⏹️ Detenido por el usuario en {progreso_actual:.1f}%')
    ui.notify(f'Ejecución detenida en {progreso_actual:.1f}%', type='warning')
    ui.navigate.to('/')


def ajustar_velocidad_proceso(nueva_velocidad, velocidad_label):
    """Ajusta la velocidad del proceso en tiempo real"""
    if not app_state.en_ejecucion:
        return

    if not app_state.receta_actual:
        return

    try:
        velocidad = int(nueva_velocidad)

        if not 1 <= velocidad <= 10:
            return

        # Obtener el proceso actual de la receta
        proceso = app_state.receta_actual.procesos[app_state.paso_actual]

        # Ajustar velocidad directamente en el proceso
        velocidad_anterior = proceso.ajustar_velocidad(velocidad)

        # Guardar en app_state para usar en el cálculo del timer
        app_state.velocidad_actual = velocidad

        # Actualizar UI
        velocidad_label.text = f'Velocidad: {velocidad}'
        agregar_log(f'⚡ Velocidad ajustada: {velocidad_anterior} → {velocidad}')

    except ValueError:
        ui.notify('Velocidad inválida', type='negative')
    except Exception as e:
        ui.notify(f'Error al ajustar velocidad: {str(e)}', type='negative')


def siguiente_paso():
    """Avanza al siguiente paso"""
    if app_state.paso_actual + 1 >= app_state.receta_actual.get_num_pasos():
        # Receta completada - mostrar pantalla de celebración
        nombre_receta = app_state.receta_actual.nombre
        agregar_log(f'🏁 Receta completada: {nombre_receta}')

        # Guardar nombre y activar celebración ANTES de resetear
        app_state.nombre_receta_completada = nombre_receta
        app_state.mostrar_celebracion = True
        app_state.receta_actual = None
        app_state.paso_actual = 0
        app_state.en_ejecucion = False
        app_state.paso_completado = False
        app_state.modo_seleccionado = None

        navegar_a('celebracion')
    else:
        app_state.siguiente_paso()
        agregar_log(f'➡️ Avanzando al paso {app_state.paso_actual + 1}')
        navegar_a('dashboard')


def cancelar_receta():
    """Cancela la receta actual"""
    agregar_log('❌ Receta cancelada')
    app_state.reset_execution()
    ui.notify('Receta cancelada', type='warning')
    navegar_a('dashboard')


# ===== VISTA: CONFIG =====
def renderizar_config():
    """Panel de configuración"""
    with ui.row().classes('w-full items-center gap-3 mb-4'):
        ui.button(icon='arrow_back', on_click=lambda: navegar_a('dashboard')).props('flat round').style(
            f'color: {COLORS.CYAN};'
        )
        ui.label('CONFIGURACIÓN').style(
            f'font-size: 1.3rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY}; '
            f'text-shadow: 0 0 10px {COLORS.CYAN};'
        )

    with ui.element('div').classes('lcd-screen'):
        ui.label('Opciones del Sistema').style(
            f'font-size: 1.2rem; font-weight: bold; color: {COLORS.CYAN}; margin-bottom: 1.5rem;'
        )

        # Botón de reiniciar base de datos
        with ui.card().classes('w-full').style(
            f'background: {COLORS.BG_CARD}; border: 2px solid {COLORS.BORDER_PRIMARY}; padding: 1.5rem;'
        ):
            ui.label('Reiniciar Base de Datos').style(
                f'font-size: 1.1rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY}; margin-bottom: 0.5rem;'
            )
            ui.label('Elimina todas las recetas creadas por ti. Las recetas preinstaladas no se verán afectadas.').style(
                f'font-size: 0.9rem; color: {COLORS.TEXT_SECONDARY}; margin-bottom: 1rem;'
            )

            ui.button(
                'REINICIAR RECETAS DE USUARIO',
                icon='delete_forever',
                on_click=confirmar_reinicio_bd
            ).style(
                f'background: {COLORS.BTN_DANGER}; color: white; padding: 0.75rem 1.5rem; font-weight: bold;'
            )


def confirmar_reinicio_bd():
    """Muestra diálogo de confirmación para reiniciar BD"""
    with ui.dialog() as dialog, ui.card().style(f'background: {COLORS.BG_CARD}; min-width: 400px;'):
        ui.label('⚠️ CONFIRMAR REINICIO').style(
            f'font-size: 1.3rem; font-weight: bold; color: {COLORS.ORANGE}; margin-bottom: 1rem;'
        )
        ui.label('¿Estás seguro de que deseas eliminar TODAS tus recetas personalizadas?').style(
            f'font-size: 1rem; color: {COLORS.TEXT_PRIMARY}; margin-bottom: 0.5rem;'
        )
        ui.label('Esta acción NO se puede deshacer.').style(
            f'font-size: 0.9rem; color: {COLORS.MAGENTA}; margin-bottom: 1.5rem;'
        )

        with ui.row().classes('w-full justify-end gap-3'):
            ui.button('Cancelar', on_click=dialog.close).props('flat').style(
                f'color: {COLORS.TEXT_SECONDARY};'
            )
            ui.button('SÍ, ELIMINAR TODO', on_click=lambda: [reiniciar_bd_usuario(), dialog.close()]).style(
                f'background: {COLORS.BTN_STOP}; color: white;'
            )

    dialog.open()


def reiniciar_bd_usuario():
    """Reinicia la base de datos de recetas de usuario"""
    try:
        from database.db import DatabaseManager
        db = DatabaseManager()

        db.ejecutar_comando("DELETE FROM ingredientes WHERE es_base = 0")
        db.ejecutar_comando("DELETE FROM procesos_usuario")
        db.ejecutar_comando("DELETE FROM recetas_usuario")

        agregar_log('🗑️ Base de datos de usuario reiniciada')
        ui.notify('✓ Todas las recetas de usuario han sido eliminadas', type='positive', position='top')

        if app_state.receta_actual and not app_state.receta_actual.es_base:
            app_state.reset_execution()

        navegar_a('dashboard')
    except Exception as e:
        ui.notify(f'Error al reiniciar BD: {str(e)}', type='negative')


# ===== VISTA: PROCESOS PERSONALIZADOS =====
def renderizar_procesos_personalizados():
    """Editor de procesos personalizados"""
    from ui.components.custom_process_editor import mostrar_editor_procesos_personalizados

    with ui.row().classes('w-full items-center gap-3 mb-4'):
        ui.button(icon='arrow_back', on_click=lambda: navegar_a('dashboard')).props('flat round').style(
            f'color: {COLORS.CYAN};'
        )
        ui.label('FUNCIONES PERSONALIZADAS').style(
            f'font-size: 1.3rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY}; '
            f'text-shadow: 0 0 10px {COLORS.PURPLE};'
        )

    mostrar_editor_procesos_personalizados()


# ===== VISTA: BROWSER =====
def renderizar_browser():
    """Navegador de recetas"""
    with ui.row().classes('w-full items-center gap-3 mb-4'):
        ui.button(icon='arrow_back', on_click=lambda: navegar_a('dashboard')).props('flat round').style(
            f'color: {COLORS.CYAN};'
        )
        ui.label('BIBLIOTECA DE RECETAS').style(
            f'font-size: 1.3rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY}; '
            f'text-shadow: 0 0 10px {COLORS.CYAN};'
        )

    # Filtros
    with ui.row().classes('w-full gap-2 mb-4 flex-wrap'):
        filtros = [
            ('todas', 'Todas'),
            ('base', 'Preinstaladas'),
            ('usuario', 'Mis Recetas'),
            ('favoritas', 'Favoritas')
        ]

        for key, label in filtros:
            is_active = app_state.filtro_recetas == key
            btn = ui.button(label, on_click=lambda k=key: set_filtro(k)).props('dense')
            if is_active:
                btn.style(f'background: {COLORS.CYAN}; color: {COLORS.BG_PRIMARY};')
            else:
                btn.style(f'background: {COLORS.BG_CARD}; color: {COLORS.TEXT_SECONDARY}; border: 1px solid {COLORS.BORDER_PRIMARY};')

    # Grid de recetas
    recetas_base, recetas_usuario = recetas_ctrl.obtener_todas_recetas()

    filtro = app_state.filtro_recetas
    if filtro == 'base':
        recetas = recetas_base
    elif filtro == 'usuario':
        recetas = recetas_usuario
    elif filtro == 'favoritas':
        recetas = [r for r in recetas_usuario if getattr(r, 'favorito', False)]
    else:
        recetas = recetas_base + recetas_usuario

    if not recetas:
        with ui.column().classes('w-full items-center py-8'):
            ui.icon('search_off').style(f'font-size: 4rem; color: {COLORS.TEXT_SECONDARY};')
            ui.label('No hay recetas').style(f'color: {COLORS.TEXT_SECONDARY};')
    else:
        with ui.grid(columns=2).classes('w-full gap-3'):
            for receta in recetas:
                crear_card_receta(receta)


def set_filtro(filtro: str):
    """Cambia el filtro de recetas"""
    app_state.filtro_recetas = filtro
    navegar_a('browser')


def crear_card_receta(receta):
    """Crea una tarjeta de receta"""
    with ui.element('div').classes('recipe-card').on('click', lambda r=receta: cargar_receta(r)):
        with ui.row().classes('w-full items-start justify-between gap-2'):
            with ui.column().classes('flex-1 gap-1'):
                badge_text = '⭐ BASE' if receta.es_base else '👤 MIA'
                badge_color = COLORS.ORANGE if receta.es_base else COLORS.CYAN
                ui.label(badge_text).style(
                    f'font-size: 0.7rem; color: {badge_color}; font-weight: bold;'
                )

                ui.label(receta.nombre).style(
                    f'font-size: 1rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY};'
                )

                with ui.row().classes('gap-3'):
                    ui.label(f'📋 {receta.get_num_pasos()} pasos').style(
                        f'font-size: 0.8rem; color: {COLORS.TEXT_SECONDARY};'
                    )
                    duracion = receta.get_duracion_total()
                    mins = duracion // 60
                    ui.label(f'⏱ {mins}m' if mins > 0 else f'⏱ {duracion}s').style(
                        f'font-size: 0.8rem; color: {COLORS.TEXT_SECONDARY};'
                    )

            if not receta.es_base:
                is_fav = getattr(receta, 'favorito', False)
                fav_icon = 'star' if is_fav else 'star_border'
                fav_color = COLORS.ORANGE if is_fav else COLORS.TEXT_SECONDARY

                ui.button(icon=fav_icon, on_click=lambda e, r=receta: toggle_favorito(r)).props('flat dense').style(
                    f'color: {fav_color};'
                )


def toggle_favorito(receta):
    """Toggle favorito"""
    try:
        nuevo_estado = recetas_ctrl.toggle_favorito(receta.id, receta.es_base)
        receta.favorito = nuevo_estado
        msg = 'Agregada a favoritos' if nuevo_estado else 'Eliminada de favoritos'
        ui.notify(msg, type='positive', position='top')
        navegar_a('browser')
    except Exception as e:
        ui.notify(f'Error: {str(e)}', type='negative')


def cargar_receta(receta):
    """Carga una receta"""
    app_state.cargar_receta(receta)
    agregar_log(f'📖 Receta cargada: {receta.nombre}')
    ui.notify(f'Receta cargada: {receta.nombre}', type='positive', position='top')
    navegar_a('dashboard')


# ===== VISTA: WIZARD =====
def renderizar_wizard():
    """Wizard de creación de recetas"""

    # Header
    with ui.row().classes('w-full items-center gap-3 mb-4'):
        ui.button(icon='arrow_back', on_click=cancelar_wizard).props('flat round').style(
            f'color: {COLORS.CYAN};'
        )
        ui.label('CREAR RECETA').style(
            f'font-size: 1.3rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY}; '
            f'text-shadow: 0 0 10px {COLORS.CYAN};'
        )

    # Indicador de paso
    paso_actual = app_state.wizard_paso
    with ui.row().classes('w-full justify-center gap-4 mb-6'):
        for i in range(1, 4):
            is_active = i == paso_actual
            is_done = i < paso_actual

            color = COLORS.CYAN if is_active else (COLORS.GREEN if is_done else COLORS.BORDER_PRIMARY)

            with ui.element('div').style(
                f'width: 40px; height: 40px; border-radius: 50%; '
                f'background: {color if is_active or is_done else COLORS.BG_CARD}; '
                f'border: 2px solid {color}; '
                f'display: flex; align-items: center; justify-content: center; '
                f'{"box-shadow: 0 0 15px " + COLORS.CYAN + ";" if is_active else ""}'
            ):
                if is_done:
                    ui.icon('check').style('color: white; font-size: 1.2rem;')
                else:
                    ui.label(str(i)).style(
                        f'color: {"white" if is_active else COLORS.TEXT_SECONDARY}; '
                        f'font-weight: bold;'
                    )

    # Contenido del paso
    with ui.element('div').classes('lcd-screen'):
        if paso_actual == 1:
            renderizar_wizard_paso1()
        elif paso_actual == 2:
            renderizar_wizard_paso2()
        elif paso_actual == 3:
            renderizar_wizard_paso3()


def renderizar_wizard_paso1():
    """Paso 1: Información básica"""
    ui.label('Información Básica').style(
        f'font-size: 1.2rem; font-weight: bold; color: {COLORS.CYAN}; margin-bottom: 1rem;'
    )

    # Nombre
    ui.label('Nombre de la receta *').style(f'color: {COLORS.TEXT_SECONDARY}; margin-bottom: 0.5rem;')
    nombre_input = ui.input(placeholder='Ej: Gazpacho Andaluz').props('outlined dark').classes('w-full')
    nombre_input.style(f'color: {COLORS.TEXT_PRIMARY};')

    ui.space()

    # Descripción
    ui.label('Descripción (opcional)').style(f'color: {COLORS.TEXT_SECONDARY}; margin-bottom: 0.5rem;')
    desc_input = ui.textarea(placeholder='Describe tu receta...').props('outlined dark').classes('w-full')

    # Guardar referencias
    app_state.wizard_nombre_input = nombre_input
    app_state.wizard_desc_input = desc_input

    # Botones
    with ui.row().classes('w-full justify-end gap-3 mt-6'):
        ui.button('Cancelar', on_click=cancelar_wizard).props('flat').style(f'color: {COLORS.TEXT_SECONDARY};')
        ui.button('Siguiente', icon='arrow_forward', on_click=wizard_siguiente).style(
            f'background: {COLORS.BTN_ACTION}; color: white;'
        )


def renderizar_wizard_paso2():
    """Paso 2: Ingredientes"""
    ui.label('Ingredientes').style(
        f'font-size: 1.2rem; font-weight: bold; color: {COLORS.CYAN}; margin-bottom: 1rem;'
    )

    # Lista de ingredientes agregados
    if app_state.wizard_ingredientes:
        for i, ing in enumerate(app_state.wizard_ingredientes):
            with ui.row().classes('w-full items-center gap-2 mb-2'):
                ui.label(f"• {ing['nombre']} - {ing['cantidad']} {ing['unidad']}").style(
                    f'color: {COLORS.TEXT_PRIMARY}; flex: 1;'
                )
                ui.button(icon='delete', on_click=lambda idx=i: eliminar_ingrediente(idx)).props('flat dense').style(
                    f'color: {COLORS.MAGENTA};'
                )

    # Formulario para agregar
    ui.label('Agregar ingrediente:').style(f'color: {COLORS.TEXT_SECONDARY}; margin-top: 1rem;')

    with ui.row().classes('w-full gap-2 items-end'):
        nombre_ing = ui.input(placeholder='Ingrediente').props('outlined dark dense').classes('flex-1')
        cantidad_ing = ui.input(placeholder='Cant.').props('outlined dark dense type=number').style('width: 80px;')
        unidad_ing = ui.select(['g', 'kg', 'ml', 'l', 'unidad'], value='g').props('outlined dark dense').style('width: 80px;')

        ui.button(icon='add', on_click=lambda: agregar_ingrediente(nombre_ing, cantidad_ing, unidad_ing)).props('round dense').style(
            f'background: {COLORS.CYAN}; color: white;'
        )

    # Botones navegación
    with ui.row().classes('w-full justify-between mt-6'):
        ui.button('Atrás', icon='arrow_back', on_click=wizard_anterior).props('flat').style(f'color: {COLORS.TEXT_SECONDARY};')
        ui.button('Siguiente', icon='arrow_forward', on_click=wizard_siguiente).style(
            f'background: {COLORS.BTN_ACTION}; color: white;'
        )


def renderizar_wizard_paso3():
    """Paso 3: Procesos"""
    from models.procesos_basicos import _procesos_personalizados_cache

    ui.label('Pasos de Cocción').style(
        f'font-size: 1.2rem; font-weight: bold; color: {COLORS.CYAN}; margin-bottom: 1rem;'
    )

    # Lista de procesos
    if app_state.wizard_procesos:
        for i, proc in enumerate(app_state.wizard_procesos):
            with ui.row().classes('w-full items-center gap-2 mb-2'):
                ui.label(f"{i+1}. {proc['tipo']} - {proc['duracion']}s").style(
                    f'color: {COLORS.TEXT_PRIMARY}; flex: 1;'
                )
                ui.button(icon='delete', on_click=lambda idx=i: eliminar_proceso(idx)).props('flat dense').style(
                    f'color: {COLORS.MAGENTA};'
                )

    # Selector de modo - incluye modos básicos + funciones personalizadas
    ui.label('Agregar paso:').style(f'color: {COLORS.TEXT_SECONDARY}; margin-top: 1rem;')

    # Modos básicos
    modos_basicos = ['Picar', 'Rallar', 'Triturar', 'Trocear', 'Amasar', 'Hervir', 'Sofreir', 'Vapor', 'PrepararPure', 'Pesar']

    # Añadir funciones personalizadas
    modos_personalizados = list(_procesos_personalizados_cache.keys())
    modos = modos_basicos + modos_personalizados

    with ui.row().classes('w-full gap-2 items-end flex-wrap'):
        modo_select = ui.select(modos, value='Picar', label='Modo').props('outlined dark dense')
        duracion_proc = ui.input(placeholder='Seg', value='5').props('outlined dark dense type=number').style('width: 80px;')

        ui.button(icon='add', on_click=lambda: agregar_proceso(modo_select, duracion_proc)).props('round dense').style(
            f'background: {COLORS.CYAN}; color: white;'
        )

    # Botones navegación
    with ui.row().classes('w-full justify-between mt-6'):
        ui.button('Atrás', icon='arrow_back', on_click=wizard_anterior).props('flat').style(f'color: {COLORS.TEXT_SECONDARY};')
        ui.button('GUARDAR', icon='save', on_click=guardar_receta).style(
            f'background: {COLORS.BTN_POWER}; color: white;'
        )


def agregar_ingrediente(nombre_input, cantidad_input, unidad_input):
    """Agrega un ingrediente"""
    nombre = nombre_input.value
    cantidad = cantidad_input.value
    unidad = unidad_input.value

    if not nombre or not cantidad:
        ui.notify('Completa nombre y cantidad', type='warning')
        return

    app_state.wizard_ingredientes.append({
        'nombre': nombre,
        'cantidad': float(cantidad),
        'unidad': unidad
    })

    nombre_input.value = ''
    cantidad_input.value = ''

    ui.notify(f'Ingrediente agregado: {nombre}', type='positive')
    navegar_a('wizard')


def eliminar_ingrediente(idx):
    """Elimina un ingrediente"""
    app_state.wizard_ingredientes.pop(idx)
    navegar_a('wizard')


def agregar_proceso(modo_select, duracion_input):
    """Agrega un proceso"""
    modo = modo_select.value
    duracion = duracion_input.value

    if not duracion:
        ui.notify('Indica la duración', type='warning')
        return

    app_state.wizard_procesos.append({
        'tipo': modo,
        'duracion': int(duracion),
        'parametros': ''
    })

    duracion_input.value = '5'

    ui.notify(f'Paso agregado: {modo}', type='positive')
    navegar_a('wizard')


def eliminar_proceso(idx):
    """Elimina un proceso"""
    app_state.wizard_procesos.pop(idx)
    navegar_a('wizard')


def wizard_siguiente():
    """Avanza al siguiente paso del wizard"""
    paso = app_state.wizard_paso

    # Validaciones
    if paso == 1:
        nombre = getattr(app_state, 'wizard_nombre_input', None)
        desc = getattr(app_state, 'wizard_desc_input', None)

        if nombre and nombre.value:
            app_state.wizard_nombre = nombre.value
            app_state.wizard_descripcion = desc.value if desc else ''
        else:
            ui.notify('Introduce un nombre para la receta', type='warning')
            return

    if paso < 3:
        app_state.wizard_paso = paso + 1
        navegar_a('wizard')


def wizard_anterior():
    """Retrocede al paso anterior"""
    if app_state.wizard_paso > 1:
        app_state.wizard_paso -= 1
        navegar_a('wizard')


def cancelar_wizard():
    """Cancela el wizard"""
    app_state.reset_wizard()
    navegar_a('dashboard')


def guardar_receta():
    """Guarda la receta en la base de datos"""
    nombre = getattr(app_state, 'wizard_nombre', '')
    descripcion = getattr(app_state, 'wizard_descripcion', '')

    if not nombre:
        ui.notify('Falta el nombre de la receta', type='warning')
        return

    if not app_state.wizard_procesos:
        ui.notify('Agrega al menos un paso de cocción', type='warning')
        return

    try:
        # Crear receta
        receta = recetas_ctrl.crear_receta_usuario(nombre, descripcion)

        # Agregar ingredientes
        for i, ing in enumerate(app_state.wizard_ingredientes):
            recetas_ctrl.agregar_ingrediente(
                receta.id, ing['nombre'], ing['cantidad'], ing['unidad'], i
            )

        # Agregar procesos
        for proc in app_state.wizard_procesos:
            recetas_ctrl.agregar_proceso_a_receta(
                receta.id, proc['tipo'], proc['parametros'], proc['duracion']
            )

        agregar_log(f'✅ Receta creada: {nombre}')
        ui.notify(f'Receta "{nombre}" creada con éxito!', type='positive')
        app_state.reset_wizard()
        navegar_a('browser')

    except Exception as e:
        ui.notify(f'Error: {str(e)}', type='negative')
