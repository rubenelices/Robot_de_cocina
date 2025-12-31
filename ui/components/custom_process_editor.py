"""
Editor de Procesos Personalizados
Permite a los usuarios crear y gestionar nuevas funciones de cocina
Diseño coherente con la interfaz Thermomix
"""
from nicegui import ui
from database.db import DatabaseManager
from models.procesos_basicos import (
    registrar_proceso_personalizado,
    cargar_procesos_personalizados_desde_bd,
    _procesos_personalizados_cache
)
from typing import Optional


# Colores coherentes con Thermomix
class EditorColors:
    BG_PRIMARY = '#0a0e27'
    BG_SECONDARY = '#1a1f3a'
    BG_CARD = '#1e2640'
    BG_INPUT = '#0d1117'
    CYAN = '#00d9ff'
    MAGENTA = '#ff006e'
    GREEN = '#00ff88'
    ORANGE = '#ff9500'
    PURPLE = '#a855f7'
    TEXT_PRIMARY = '#ffffff'
    TEXT_SECONDARY = '#a8b2d1'
    BORDER_PRIMARY = '#2a3f5f'
    BORDER_ACCENT = '#00d9ff'


COLORS = EditorColors()


class EditorProcesosPersonalizados:
    """Componente para crear y editar procesos personalizados"""

    def __init__(self):
        self.db = DatabaseManager()
        self.proceso_editando: Optional[dict] = None

        # Emojis predefinidos para selección rápida
        self.emojis_comunes = [
            '🥄', '🍳', '🔪', '🧀', '🥖', '🍲', '⚡', '💨',
            '🌡️', '⏱️', '🥣', '🍴', '🔥', '❄️', '💧', '🌀'
        ]

    def mostrar(self):
        """Muestra el editor completo de procesos personalizados"""

        # CSS para forzar el fondo oscuro en los inputs (más específico para Quasar)
        ui.add_head_html(f'''
        <style>
            .dark-input .q-field__control,
            .dark-input .q-field__native,
            .dark-input .q-field__control input,
            .dark-input input,
            .dark-input textarea {{
                background-color: {COLORS.BG_INPUT} !important;
                color: {COLORS.TEXT_PRIMARY} !important;
            }}
            .dark-input .q-field__control {{
                background-color: {COLORS.BG_INPUT} !important;
            }}
            .dark-input .q-field--filled .q-field__control,
            .dark-input .q-field--outlined .q-field__control {{
                background-color: {COLORS.BG_INPUT} !important;
            }}
            .dark-input .q-field--filled .q-field__control:before,
            .dark-input .q-field--outlined .q-field__control:before {{
                background-color: {COLORS.BG_INPUT} !important;
                border-color: {COLORS.BORDER_PRIMARY} !important;
            }}
            .dark-input .q-field--focused .q-field__control:before {{
                border-color: {COLORS.CYAN} !important;
            }}
            .dark-input .q-field__marginal {{
                color: {COLORS.TEXT_SECONDARY} !important;
            }}
        </style>
        ''')

        # Contenedor principal con márgenes
        with ui.column().classes('w-full items-center gap-4').style(
            f'padding: 1rem 2rem; max-width: 900px; margin: 0 auto;'
        ):

            # Formulario de creación
            with ui.element('div').style(f'''
                background: {COLORS.BG_CARD};
                border: 2px solid {COLORS.BORDER_PRIMARY};
                border-radius: 16px;
                padding: 1.5rem 2rem;
                width: 100%;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            '''):
                ui.label('CREAR NUEVA FUNCIÓN').style(
                    f'font-size: 1.2rem; font-weight: bold; color: {COLORS.CYAN}; '
                    f'margin-bottom: 1.5rem; text-align: center; display: block; '
                    f'text-shadow: 0 0 10px {COLORS.CYAN};'
                )

                # Fila 1: Nombre y Emoji lado a lado
                with ui.row().classes('w-full gap-4 items-start'):
                    # Nombre (más grande)
                    with ui.column().classes('flex-grow gap-1'):
                        ui.label('Nombre de la función').style(
                            f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.9rem; font-weight: 500;'
                        )
                        nombre_input = ui.input(placeholder='ej: Batir, Emulsionar...').classes('dark-input').style(f'''
                            width: 100%;
                        ''').props('dark outlined dense bg-color="{COLORS.BG_INPUT}"')

                    # Emoji (columna más pequeña)
                    with ui.column().classes('gap-1').style('width: 100px;'):
                        ui.label('Emoji').style(
                            f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.9rem; font-weight: 500;'
                        )
                        emoji_input = ui.input(value='⚙️').classes('dark-input').style(f'''
                            text-align: center;
                            font-size: 1.8rem;
                        ''').props('dark outlined dense')

                # Selector de emojis rápido
                ui.label('Emojis rápidos:').style(
                    f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.8rem; margin-top: 0.75rem;'
                )
                with ui.row().classes('w-full gap-1 flex-wrap'):
                    for emoji in self.emojis_comunes:
                        ui.button(emoji, on_click=lambda e=emoji: emoji_input.set_value(e)).style(f'''
                            background: {COLORS.BG_INPUT};
                            border: 1px solid {COLORS.BORDER_PRIMARY};
                            min-width: 40px;
                            height: 40px;
                            padding: 0;
                            font-size: 1.3rem;
                            border-radius: 8px;
                        ''').props('flat dense')

                # Separador visual
                ui.element('hr').style(
                    f'border: none; border-top: 1px solid {COLORS.BORDER_PRIMARY}; margin: 1rem 0;'
                )

                # Fila 2: Duración, Parámetros y Descripción en una línea
                with ui.row().classes('w-full gap-4 items-start'):
                    with ui.column().classes('gap-1').style('width: 120px;'):
                        ui.label('Duración (seg)').style(
                            f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.9rem; font-weight: 500;'
                        )
                        duracion_input = ui.number(value=5, min=1, max=3600, step=1).classes('dark-input').props('dark outlined dense')

                    with ui.column().classes('gap-1').style('width: 200px;'):
                        ui.label('Parámetros (opcional)').style(
                            f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.9rem; font-weight: 500;'
                        )
                        parametros_input = ui.input(placeholder='ej: velocidad=alta').classes('dark-input').style(f'''
                            width: 100%;
                        ''').props('dark outlined dense')

                    with ui.column().classes('flex-grow gap-1'):
                        ui.label('Descripción (opcional)').style(
                            f'color: {COLORS.TEXT_SECONDARY}; font-size: 0.9rem; font-weight: 500;'
                        )
                        descripcion_input = ui.input(placeholder='Breve descripción de la función...').classes('dark-input').style(f'''
                            width: 100%;
                        ''').props('dark outlined dense')

                # Botones de acción centrados con margen
                with ui.row().classes('w-full justify-center gap-4 mt-4 mb-2'):
                    ui.button('LIMPIAR', icon='clear', on_click=lambda: self._limpiar_formulario(
                        nombre_input, descripcion_input, duracion_input,
                        emoji_input, parametros_input
                    )).style(f'''
                        background: {COLORS.BG_SECONDARY};
                        border: 2px solid {COLORS.BORDER_PRIMARY};
                        color: {COLORS.TEXT_SECONDARY};
                        padding: 0.6rem 1.8rem;
                        border-radius: 10px;
                        font-weight: 500;
                    ''')

                    ui.button('GUARDAR FUNCIÓN', icon='save', on_click=lambda: self._guardar_proceso(
                        nombre_input.value,
                        emoji_input.value,
                        int(duracion_input.value) if duracion_input.value else 5,
                        parametros_input.value,
                        descripcion_input.value,
                        nombre_input, descripcion_input, duracion_input,
                        emoji_input, parametros_input
                    )).style(f'''
                        background: linear-gradient(135deg, {COLORS.GREEN} 0%, #00d9a0 100%);
                        color: {COLORS.BG_PRIMARY};
                        font-weight: bold;
                        padding: 0.6rem 1.8rem;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
                    ''')

            # Lista de procesos personalizados
            self.container_procesos = ui.element('div').style(f'''
                background: {COLORS.BG_CARD};
                border: 2px solid {COLORS.BORDER_PRIMARY};
                border-radius: 16px;
                padding: 1.5rem 2rem;
                width: 100%;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            ''')
            self._actualizar_lista_procesos()

    def _limpiar_formulario(self, nombre, descripcion, duracion, emoji, parametros):
        """Limpia todos los campos del formulario"""
        nombre.set_value('')
        descripcion.set_value('')
        duracion.set_value(5)
        emoji.set_value('⚙️')
        parametros.set_value('')

    def _guardar_proceso(self, nombre: str, emoji: str, duracion: int,
                        parametros: str, descripcion: str,
                        nombre_input, descripcion_input, duracion_input,
                        emoji_input, parametros_input):
        """Guarda un nuevo proceso personalizado en la base de datos"""

        # Validaciones
        if not nombre or nombre.strip() == '':
            ui.notify('El nombre del proceso es obligatorio', type='warning')
            return

        nombre = nombre.strip()

        if not emoji or emoji.strip() == '':
            emoji = '⚙️'

        if duracion < 1:
            ui.notify('La duración debe ser al menos 1 segundo', type='warning')
            return

        # Verificar si ya existe (incluyendo inactivos para evitar UNIQUE constraint)
        existente = self._verificar_nombre_existe(nombre)
        if existente:
            ui.notify(f'Ya existe una función con el nombre "{nombre}"', type='warning')
            return

        try:
            # Guardar en base de datos
            self.db.insertar_proceso_personalizado(
                nombre=nombre,
                emoji=emoji.strip(),
                duracion_base=duracion,
                parametros_defecto=parametros.strip() if parametros else "",
                descripcion=descripcion.strip() if descripcion else ""
            )

            # Registrar en el sistema en memoria
            registrar_proceso_personalizado(
                nombre=nombre,
                emoji=emoji.strip(),
                duracion_base=duracion,
                parametros_defecto=parametros.strip() if parametros else "",
                descripcion=descripcion.strip() if descripcion else ""
            )

            ui.notify(f'Función "{nombre}" creada correctamente', type='positive', position='top')

            # Limpiar formulario
            self._limpiar_formulario(
                nombre_input, descripcion_input, duracion_input,
                emoji_input, parametros_input
            )

            # Actualizar lista
            self._actualizar_lista_procesos()

        except Exception as e:
            ui.notify(f'Error al guardar: {str(e)}', type='negative')

    def _verificar_nombre_existe(self, nombre: str) -> bool:
        """Verifica si ya existe un proceso con ese nombre (activo o inactivo)"""
        query = "SELECT COUNT(*) as count FROM procesos_personalizados WHERE nombre = ?"
        result = self.db.ejecutar_query(query, (nombre,))
        return result[0]['count'] > 0

    def _actualizar_lista_procesos(self):
        """Actualiza la lista de procesos personalizados"""
        self.container_procesos.clear()

        procesos = self.db.obtener_procesos_personalizados()

        with self.container_procesos:
            ui.label('FUNCIONES CREADAS').style(
                f'font-size: 1.2rem; font-weight: bold; color: {COLORS.CYAN}; '
                f'margin-bottom: 1rem; text-align: center; display: block; '
                f'text-shadow: 0 0 10px {COLORS.CYAN};'
            )

            if not procesos:
                with ui.element('div').style(
                    f'text-align: center; padding: 2rem; color: {COLORS.TEXT_SECONDARY};'
                ):
                    ui.icon('info', size='xl').style(f'color: {COLORS.TEXT_SECONDARY}; opacity: 0.5;')
                    ui.label('No hay funciones personalizadas creadas').style(
                        f'display: block; margin-top: 0.5rem;'
                    )
                return

            with ui.column().classes('w-full gap-3'):
                for proceso in procesos:
                    self._crear_tarjeta_proceso(proceso)

    def _crear_tarjeta_proceso(self, proceso: dict):
        """Crea una tarjeta para un proceso personalizado"""
        with ui.element('div').style(f'''
            background: {COLORS.BG_INPUT};
            border: 2px solid {COLORS.BORDER_PRIMARY};
            border-radius: 12px;
            padding: 1rem 1.25rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: border-color 0.2s;
        ''').classes('hover:border-cyan-500'):
            # Emoji grande
            ui.label(proceso['emoji']).style('font-size: 2.5rem; min-width: 50px; text-align: center;')

            # Info del proceso
            with ui.column().classes('flex-grow gap-1'):
                ui.label(proceso['nombre']).style(
                    f'font-size: 1.1rem; font-weight: bold; color: {COLORS.TEXT_PRIMARY};'
                )
                if proceso['descripcion']:
                    ui.label(proceso['descripcion']).style(
                        f'font-size: 0.85rem; color: {COLORS.TEXT_SECONDARY}; line-height: 1.3;'
                    )
                with ui.row().classes('gap-4 mt-1'):
                    ui.label(f"⏱️ {proceso['duracion_base']}s").style(
                        f'font-size: 0.8rem; color: {COLORS.ORANGE}; font-weight: 500;'
                    )
                    if proceso['parametros_defecto']:
                        ui.label(f"⚙️ {proceso['parametros_defecto']}").style(
                            f'font-size: 0.8rem; color: {COLORS.TEXT_SECONDARY};'
                        )

            # Botón eliminar
            ui.button(icon='delete', on_click=lambda p=proceso: self._eliminar_proceso(p['id'], p['nombre'])).style(f'''
                background: transparent;
                color: {COLORS.MAGENTA};
                min-width: 44px;
                height: 44px;
            ''').props('flat round').tooltip('Eliminar función')

    def _eliminar_proceso(self, proceso_id: int, nombre: str):
        """Elimina un proceso personalizado (eliminación real, no soft delete)"""
        try:
            # Eliminar completamente de la base de datos
            self.db.ejecutar_comando(
                "DELETE FROM procesos_personalizados WHERE id = ?",
                (proceso_id,)
            )

            # Eliminar del cache en memoria
            if nombre in _procesos_personalizados_cache:
                del _procesos_personalizados_cache[nombre]

            ui.notify(f'Función "{nombre}" eliminada', type='positive')

            # Actualizar lista visual
            self._actualizar_lista_procesos()

        except Exception as e:
            ui.notify(f'Error al eliminar: {str(e)}', type='negative')


def mostrar_editor_procesos_personalizados():
    """Función helper para mostrar el editor"""
    editor = EditorProcesosPersonalizados()
    editor.mostrar()
