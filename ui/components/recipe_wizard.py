"""
Wizard de creación de recetas en 3 pasos
Permite crear recetas personalizadas con todos los campos necesarios
"""

from nicegui import ui
from ui.state.app_state import app_state
from ui.styles.colors import COLORS, MODO_ICONOS
from ui.components.common import show_success_notification, show_error_notification
from controllers.recetas_controller import RecetasController
from typing import Dict, Any, Optional, Callable
import re


class RecipeWizard:
    """Wizard de creación de recetas paso a paso"""

    def __init__(self, recetas_ctrl: RecetasController, on_complete: Optional[Callable] = None):
        """
        Args:
            recetas_ctrl: Controlador de recetas
            on_complete: Callback cuando se completa la creación
        """
        self.recetas_ctrl = recetas_ctrl
        self.on_complete = on_complete
        self.container = None
        self.step_content = None

        # Datos temporales del wizard
        self.recipe_data = {
            'nombre': '',
            'descripcion': '',
            'ingredientes': [],
            'procesos': []
        }

    def render(self):
        """Renderiza el wizard completo"""
        self.container = ui.column().classes('w-full h-full gap-0')

        with self.container:
            # Header con indicador de progreso
            self._render_header()

            # Contenido del paso actual
            self.step_content = ui.column().classes('w-full flex-1 p-8')

            with self.step_content:
                self._render_current_step()

        return self.container

    def _render_header(self):
        """Header con progreso y título"""
        with ui.card().classes(
            'w-full bg-white dark:bg-gray-800 rounded-none '
            'border-b-4 border-thermo-cyan-500 shadow-lg p-6'
        ):
            # Título principal
            with ui.row().classes('w-full items-center justify-between mb-6'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('restaurant_menu').classes('text-5xl text-thermo-cyan-500')
                    ui.label('Crear Nueva Receta').classes(
                        'text-4xl font-bold text-thermo-navy-700 dark:text-white'
                    )

                # Botón cerrar
                ui.button(
                    icon='close',
                    on_click=self._cancel_wizard
                ).props('flat round').classes(
                    'text-gray-600 dark:text-gray-400 hover:text-red-500'
                )

            # Indicador de progreso (3 steps)
            self._render_progress_indicator()

    def _render_progress_indicator(self):
        """Barra de progreso con 3 pasos"""
        current_step = app_state.wizard_paso

        steps = [
            {'num': 1, 'label': 'Información Básica', 'icon': 'info'},
            {'num': 2, 'label': 'Ingredientes', 'icon': 'shopping_cart'},
            {'num': 3, 'label': 'Pasos de Cocción', 'icon': 'format_list_numbered'}
        ]

        with ui.row().classes('w-full items-center justify-between gap-4'):
            for i, step in enumerate(steps):
                # Circle con número
                is_current = step['num'] == current_step
                is_completed = step['num'] < current_step

                circle_classes = [
                    'flex items-center justify-center',
                    'w-12 h-12 rounded-full',
                    'font-bold text-lg',
                    'transition-all duration-300'
                ]

                if is_current:
                    circle_classes.extend([
                        'bg-thermo-cyan-500 text-white',
                        'ring-4 ring-thermo-cyan-300 dark:ring-thermo-cyan-700',
                        'scale-110'
                    ])
                elif is_completed:
                    circle_classes.extend([
                        'bg-green-500 text-white',
                        'shadow-lg'
                    ])
                else:
                    circle_classes.extend([
                        'bg-gray-200 dark:bg-gray-700',
                        'text-gray-600 dark:text-gray-400'
                    ])

                with ui.column().classes('items-center gap-2'):
                    # Círculo
                    with ui.element('div').classes(' '.join(circle_classes)):
                        if is_completed:
                            ui.icon('check').classes('text-2xl')
                        else:
                            ui.label(str(step['num']))

                    # Label
                    label_color = (
                        'text-thermo-cyan-600 dark:text-thermo-cyan-400 font-bold'
                        if is_current else
                        'text-green-600 dark:text-green-400 font-semibold'
                        if is_completed else
                        'text-gray-500 dark:text-gray-500'
                    )
                    ui.label(step['label']).classes(f'text-sm {label_color}')

                # Línea conectora (excepto después del último)
                if i < len(steps) - 1:
                    line_color = (
                        'bg-green-500'
                        if step['num'] < current_step else
                        'bg-gray-300 dark:bg-gray-700'
                    )
                    ui.element('div').classes(
                        f'flex-1 h-1 {line_color} mx-2'
                    ).style('margin-top: 1.5rem;')

    def _render_current_step(self):
        """Renderiza el contenido del paso actual"""
        current_step = app_state.wizard_paso

        if current_step == 1:
            self._render_step_1_basic_info()
        elif current_step == 2:
            self._render_step_2_ingredients()
        elif current_step == 3:
            self._render_step_3_processes()

    # ===== PASO 1: INFORMACIÓN BÁSICA =====
    def _render_step_1_basic_info(self):
        """Paso 1: Nombre y descripción"""
        with ui.column().classes('w-full max-w-3xl mx-auto gap-8'):
            # Título del paso
            ui.label('📝 Información Básica de la Receta').classes(
                'text-3xl font-bold text-gray-900 dark:text-white mb-4'
            )

            # Card con formulario
            with ui.card().classes(
                'w-full bg-white dark:bg-gray-800 rounded-2xl p-8 '
                'border border-gray-200 dark:border-gray-700 shadow-lg'
            ):
                # Nombre
                ui.label('Nombre de la Receta *').classes(
                    'text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2'
                )
                self.nombre_input = ui.input(
                    placeholder='Ej: Gazpacho Andaluz',
                    value=self.recipe_data['nombre']
                ).props('outlined').classes('w-full text-lg')

                ui.space()

                # Descripción
                ui.label('Descripción (opcional)').classes(
                    'text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2'
                )
                self.descripcion_input = ui.textarea(
                    placeholder='Describe brevemente tu receta...',
                    value=self.recipe_data['descripcion']
                ).props('outlined rows=4').classes('w-full')

                # Info helper
                with ui.row().classes('items-center gap-2 mt-4 p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20'):
                    ui.icon('info').classes('text-blue-600 dark:text-blue-400')
                    ui.label(
                        'Elige un nombre descriptivo y único para tu receta. '
                        'La descripción ayudará a recordar para qué sirve.'
                    ).classes('text-sm text-blue-700 dark:text-blue-300')

            # Botones de navegación
            self._render_step_navigation(can_continue=lambda: len(self.nombre_input.value.strip() if self.nombre_input.value else '') > 0)

    # ===== PASO 2: INGREDIENTES =====
    def _render_step_2_ingredients(self):
        """Paso 2: Lista de ingredientes"""
        with ui.column().classes('w-full max-w-4xl mx-auto gap-8'):
            # Título
            ui.label('🛒 Ingredientes de la Receta').classes(
                'text-3xl font-bold text-gray-900 dark:text-white mb-4'
            )

            # Card con lista de ingredientes
            with ui.card().classes(
                'w-full bg-white dark:bg-gray-800 rounded-2xl p-8 '
                'border border-gray-200 dark:border-gray-700 shadow-lg'
            ):
                # Lista actual de ingredientes
                if app_state.wizard_ingredientes:
                    ui.label('Ingredientes agregados:').classes(
                        'text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4'
                    )

                    ingredientes_container = ui.column().classes('w-full gap-3 mb-6')
                    with ingredientes_container:
                        for idx, ingrediente in enumerate(app_state.wizard_ingredientes):
                            self._render_ingrediente_item(idx, ingrediente)
                else:
                    with ui.column().classes('w-full items-center py-8'):
                        ui.icon('shopping_cart').classes('text-6xl text-gray-400')
                        ui.label('No hay ingredientes agregados aún').classes(
                            'text-lg text-gray-500 dark:text-gray-500'
                        )

                ui.separator().classes('my-6 bg-gray-300 dark:bg-gray-700')

                # Formulario para agregar ingrediente
                ui.label('Agregar Nuevo Ingrediente').classes(
                    'text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4'
                )

                with ui.grid().classes('grid-cols-1 md:grid-cols-3 gap-4 items-end'):
                    # Nombre
                    nombre_input = ui.input(
                        label='Ingrediente',
                        placeholder='Ej: Tomate'
                    ).props('outlined').classes('w-full')

                    # Cantidad
                    cantidad_input = ui.input(
                        label='Cantidad',
                        placeholder='500'
                    ).props('outlined type=number').classes('w-full')

                    # Unidad
                    unidad_input = ui.select(
                        label='Unidad',
                        options=['g', 'kg', 'ml', 'l', 'unidad', 'cucharada', 'pizca'],
                        value='g'
                    ).props('outlined').classes('w-full')

                # Botón agregar
                ui.button(
                    'Agregar Ingrediente',
                    icon='add_circle',
                    on_click=lambda: self._add_ingrediente(
                        nombre_input.value,
                        cantidad_input.value,
                        unidad_input.value,
                        nombre_input,
                        cantidad_input
                    )
                ).props('unelevated').classes(
                    'w-full md:w-auto bg-thermo-cyan-500 hover:bg-thermo-cyan-600 '
                    'text-white px-8 py-3 rounded-xl font-semibold mt-4'
                )

            # Botones de navegación
            self._render_step_navigation(can_continue=lambda: len(app_state.wizard_ingredientes) > 0)

    def _render_ingrediente_item(self, idx: int, ingrediente: Dict[str, Any]):
        """Renderiza un item de ingrediente en la lista"""
        with ui.card().classes(
            'w-full bg-gray-50 dark:bg-gray-900 rounded-xl p-4 '
            'border border-gray-200 dark:border-gray-700'
        ):
            with ui.row().classes('w-full items-center justify-between'):
                # Info del ingrediente
                with ui.row().classes('items-center gap-3 flex-1'):
                    ui.icon('restaurant').classes('text-thermo-cyan-500 text-2xl')
                    with ui.column().classes('gap-1'):
                        ui.label(ingrediente['nombre']).classes(
                            'text-lg font-bold text-gray-900 dark:text-white'
                        )
                        ui.label(
                            f"{ingrediente['cantidad']} {ingrediente['unidad']}"
                        ).classes('text-sm text-gray-600 dark:text-gray-400')

                # Botón eliminar
                ui.button(
                    icon='delete',
                    on_click=lambda i=idx: self._remove_ingrediente(i)
                ).props('flat round dense').classes(
                    'text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20'
                )

    def _add_ingrediente(self, nombre: str, cantidad: str, unidad: str, nombre_input, cantidad_input):
        """Agrega un ingrediente a la lista"""
        # Validar
        if not nombre or not nombre.strip():
            show_error_notification('⚠️ Debes especificar el nombre del ingrediente')
            return

        if not cantidad or float(cantidad) <= 0:
            show_error_notification('⚠️ La cantidad debe ser mayor a 0')
            return

        # Agregar
        app_state.wizard_ingredientes.append({
            'nombre': nombre.strip(),
            'cantidad': float(cantidad),
            'unidad': unidad
        })

        # Limpiar inputs
        nombre_input.value = ''
        cantidad_input.value = ''

        # Notificar
        show_success_notification(f'✓ Ingrediente agregado: {nombre}')

        # Refrescar vista
        self.step_content.clear()
        with self.step_content:
            self._render_current_step()

    def _remove_ingrediente(self, idx: int):
        """Elimina un ingrediente de la lista"""
        nombre = app_state.wizard_ingredientes[idx]['nombre']
        app_state.wizard_ingredientes.pop(idx)
        show_success_notification(f'Ingrediente eliminado: {nombre}')

        # Refrescar vista
        self.step_content.clear()
        with self.step_content:
            self._render_current_step()

    # ===== PASO 3: PROCESOS =====
    def _render_step_3_processes(self):
        """Paso 3: Pasos de cocción"""
        with ui.column().classes('w-full max-w-5xl mx-auto gap-8'):
            # Título
            ui.label('🔥 Pasos de Cocción').classes(
                'text-3xl font-bold text-gray-900 dark:text-white mb-4'
            )

            # Card con lista de procesos
            with ui.card().classes(
                'w-full bg-white dark:bg-gray-800 rounded-2xl p-8 '
                'border border-gray-200 dark:border-gray-700 shadow-lg'
            ):
                # Lista actual de procesos
                if app_state.wizard_procesos:
                    ui.label('Pasos agregados:').classes(
                        'text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4'
                    )

                    procesos_container = ui.column().classes('w-full gap-4 mb-6')
                    with procesos_container:
                        for idx, proceso in enumerate(app_state.wizard_procesos):
                            self._render_proceso_item(idx, proceso)
                else:
                    with ui.column().classes('w-full items-center py-8'):
                        ui.icon('format_list_numbered').classes('text-6xl text-gray-400')
                        ui.label('No hay pasos de cocción agregados aún').classes(
                            'text-lg text-gray-500 dark:text-gray-500'
                        )

                ui.separator().classes('my-6 bg-gray-300 dark:bg-gray-700')

                # Formulario para agregar proceso
                ui.label('Agregar Nuevo Paso').classes(
                    'text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4'
                )

                with ui.column().classes('w-full gap-4'):
                    # Tipo de proceso
                    tipo_select = ui.select(
                        label='Modo de Cocción',
                        options=list(MODO_ICONOS.keys()),
                        value=list(MODO_ICONOS.keys())[0]
                    ).props('outlined').classes('w-full')

                    # Agregar icono visual
                    with ui.row().classes('items-center gap-2'):
                        ui.label('Vista previa:').classes('text-sm text-gray-600 dark:text-gray-400')
                        preview_icon = ui.label(MODO_ICONOS[tipo_select.value]).classes('text-4xl')
                        preview_label = ui.label(tipo_select.value).classes(
                            'text-lg font-bold text-gray-900 dark:text-white'
                        )

                    # Actualizar preview al cambiar
                    tipo_select.on('update:model-value', lambda e: [
                        setattr(preview_icon, 'text', MODO_ICONOS[e.args]),
                        setattr(preview_label, 'text', e.args),
                        preview_icon.update(),
                        preview_label.update()
                    ])

                    # Duración
                    with ui.row().classes('items-center gap-4'):
                        duracion_input = ui.input(
                            label='Duración (segundos)',
                            placeholder='5',
                            value='5'
                        ).props('outlined type=number min=1 max=3600').classes('flex-1')

                        ui.label('segundos').classes('text-gray-600 dark:text-gray-400')

                    # Parámetros (opcional)
                    parametros_input = ui.input(
                        label='Parámetros (opcional)',
                        placeholder='Ej: velocidad=10, temperatura=80'
                    ).props('outlined').classes('w-full')

                    # Botón agregar
                    ui.button(
                        'Agregar Paso',
                        icon='add_circle',
                        on_click=lambda: self._add_proceso(
                            tipo_select.value,
                            duracion_input.value,
                            parametros_input.value,
                            duracion_input,
                            parametros_input
                        )
                    ).props('unelevated').classes(
                        'w-full md:w-auto bg-thermo-cyan-500 hover:bg-thermo-cyan-600 '
                        'text-white px-8 py-3 rounded-xl font-semibold'
                    )

            # Botones de navegación
            self._render_step_navigation(
                can_continue=lambda: len(app_state.wizard_procesos) > 0,
                is_final_step=True
            )

    def _render_proceso_item(self, idx: int, proceso: Dict[str, Any]):
        """Renderiza un item de proceso en la lista"""
        with ui.card().classes(
            'w-full bg-gradient-to-r from-thermo-cyan-50 to-blue-50 '
            'dark:from-thermo-cyan-900/20 dark:to-blue-900/20 '
            'rounded-xl p-6 border-2 border-thermo-cyan-300 dark:border-thermo-cyan-700'
        ):
            with ui.row().classes('w-full items-start justify-between gap-4'):
                # Número de paso + icono
                with ui.row().classes('items-center gap-4'):
                    # Badge de paso
                    with ui.element('div').classes(
                        'flex items-center justify-center '
                        'w-12 h-12 rounded-full '
                        'bg-thermo-cyan-500 text-white font-bold text-xl'
                    ):
                        ui.label(str(idx + 1))

                    # Icono del modo
                    ui.label(MODO_ICONOS[proceso['tipo']]).classes('text-5xl')

                    # Info del proceso
                    with ui.column().classes('gap-2 flex-1'):
                        ui.label(proceso['tipo']).classes(
                            'text-2xl font-bold text-gray-900 dark:text-white'
                        )
                        ui.label(f"⏱️ Duración: {proceso['duracion']} segundos").classes(
                            'text-sm text-gray-700 dark:text-gray-300'
                        )
                        if proceso['parametros']:
                            ui.label(f"📋 Parámetros: {proceso['parametros']}").classes(
                                'text-sm text-gray-600 dark:text-gray-400'
                            )

                # Botones de acción
                with ui.column().classes('gap-2'):
                    # Mover arriba (si no es el primero)
                    if idx > 0:
                        ui.button(
                            icon='arrow_upward',
                            on_click=lambda i=idx: self._move_proceso_up(i)
                        ).props('flat round dense').classes('text-blue-600 hover:bg-blue-50')

                    # Mover abajo (si no es el último)
                    if idx < len(app_state.wizard_procesos) - 1:
                        ui.button(
                            icon='arrow_downward',
                            on_click=lambda i=idx: self._move_proceso_down(i)
                        ).props('flat round dense').classes('text-blue-600 hover:bg-blue-50')

                    # Eliminar
                    ui.button(
                        icon='delete',
                        on_click=lambda i=idx: self._remove_proceso(i)
                    ).props('flat round dense').classes('text-red-500 hover:bg-red-50')

    def _add_proceso(self, tipo: str, duracion: str, parametros: str, duracion_input, parametros_input):
        """Agrega un proceso a la lista"""
        # Validar
        if not duracion or int(duracion) <= 0:
            show_error_notification('⚠️ La duración debe ser mayor a 0')
            return

        # Agregar
        app_state.wizard_procesos.append({
            'tipo': tipo,
            'duracion': int(duracion),
            'parametros': parametros.strip() if parametros else ''
        })

        # Limpiar inputs
        duracion_input.value = '5'
        parametros_input.value = ''

        # Notificar
        show_success_notification(f'✓ Paso agregado: {tipo}')

        # Refrescar vista
        self.step_content.clear()
        with self.step_content:
            self._render_current_step()

    def _remove_proceso(self, idx: int):
        """Elimina un proceso de la lista"""
        tipo = app_state.wizard_procesos[idx]['tipo']
        app_state.wizard_procesos.pop(idx)
        show_success_notification(f'Paso eliminado: {tipo}')

        # Refrescar vista
        self.step_content.clear()
        with self.step_content:
            self._render_current_step()

    def _move_proceso_up(self, idx: int):
        """Mueve un proceso hacia arriba en la lista"""
        if idx > 0:
            app_state.wizard_procesos[idx], app_state.wizard_procesos[idx - 1] = \
                app_state.wizard_procesos[idx - 1], app_state.wizard_procesos[idx]

            # Refrescar vista
            self.step_content.clear()
            with self.step_content:
                self._render_current_step()

    def _move_proceso_down(self, idx: int):
        """Mueve un proceso hacia abajo en la lista"""
        if idx < len(app_state.wizard_procesos) - 1:
            app_state.wizard_procesos[idx], app_state.wizard_procesos[idx + 1] = \
                app_state.wizard_procesos[idx + 1], app_state.wizard_procesos[idx]

            # Refrescar vista
            self.step_content.clear()
            with self.step_content:
                self._render_current_step()

    # ===== NAVEGACIÓN =====
    def _render_step_navigation(self, can_continue: Callable = None, is_final_step: bool = False):
        """Renderiza botones de navegación entre pasos"""
        with ui.row().classes('w-full justify-between items-center mt-8 pt-8 border-t border-gray-300 dark:border-gray-700'):
            # Botón Atrás
            if app_state.wizard_paso > 1:
                ui.button(
                    'Atrás',
                    icon='arrow_back',
                    on_click=self._previous_step
                ).props('outline').classes(
                    'text-gray-700 dark:text-gray-300 px-8 py-3 rounded-xl font-semibold'
                )
            else:
                ui.label('')  # Spacer

            # Botón Siguiente / Guardar
            can_proceed = can_continue() if can_continue else True

            if is_final_step:
                ui.button(
                    'Guardar Receta',
                    icon='check_circle',
                    on_click=self._save_recipe
                ).props('unelevated' if can_proceed else 'disable').classes(
                    'bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-xl font-semibold'
                )
            else:
                ui.button(
                    'Siguiente',
                    icon='arrow_forward',
                    on_click=self._next_step
                ).props('unelevated' if can_proceed else 'disable').classes(
                    'bg-thermo-cyan-500 hover:bg-thermo-cyan-600 text-white px-8 py-3 rounded-xl font-semibold'
                )

    def _next_step(self):
        """Avanza al siguiente paso"""
        # Guardar datos del paso 1
        if app_state.wizard_paso == 1:
            self.recipe_data['nombre'] = self.nombre_input.value if self.nombre_input.value else ''
            self.recipe_data['descripcion'] = self.descripcion_input.value if self.descripcion_input.value else ''

        if app_state.wizard_paso < 3:
            app_state.wizard_paso += 1
            self.step_content.clear()
            with self.step_content:
                self._render_current_step()

            # Re-renderizar header
            self.container.clear()
            with self.container:
                self._render_header()
                self.step_content = ui.column().classes('w-full flex-1 p-8')
                with self.step_content:
                    self._render_current_step()

    def _previous_step(self):
        """Retrocede al paso anterior"""
        if app_state.wizard_paso > 1:
            app_state.wizard_paso -= 1
            self.step_content.clear()
            with self.step_content:
                self._render_current_step()

            # Re-renderizar header
            self.container.clear()
            with self.container:
                self._render_header()
                self.step_content = ui.column().classes('w-full flex-1 p-8')
                with self.step_content:
                    self._render_current_step()

    def _cancel_wizard(self):
        """Cancela el wizard"""
        app_state.reset_wizard()
        ui.notify('Creación de receta cancelada', type='warning', position='top')

        if self.on_complete:
            self.on_complete(None)

    def _save_recipe(self):
        """Guarda la receta en la base de datos"""
        try:
            # Crear receta
            receta = self.recetas_ctrl.crear_receta_usuario(
                nombre=self.recipe_data['nombre'],
                descripcion=self.recipe_data['descripcion']
            )

            # Agregar ingredientes
            for i, ing in enumerate(app_state.wizard_ingredientes):
                self.recetas_ctrl.agregar_ingrediente(
                    receta_id=receta.id,
                    nombre=ing['nombre'],
                    cantidad=ing['cantidad'],
                    unidad=ing['unidad'],
                    orden=i
                )

            # Agregar procesos
            for proceso in app_state.wizard_procesos:
                self.recetas_ctrl.agregar_proceso_a_receta(
                    receta_id=receta.id,
                    tipo_proceso=proceso['tipo'],
                    duracion=proceso['duracion'],
                    parametros=proceso['parametros']
                )

            # Notificar éxito
            show_success_notification(f'✓ Receta "{receta.nombre}" creada con éxito')

            # Reset wizard
            app_state.reset_wizard()

            # Callback
            if self.on_complete:
                self.on_complete(receta)

        except Exception as e:
            show_error_notification(f'❌ Error al crear receta: {str(e)}')



# ===== FUNCIÓN HELPER =====
def create_recipe_wizard(recetas_ctrl: RecetasController, on_complete: Optional[Callable] = None):
    """
    Crea el wizard de creación de recetas

    Args:
        recetas_ctrl: Controlador de recetas
        on_complete: Callback cuando se completa (recibe receta creada o None si se cancela)

    Returns:
        RecipeWizard instance
    """
    wizard = RecipeWizard(recetas_ctrl, on_complete)
    return wizard.render()
