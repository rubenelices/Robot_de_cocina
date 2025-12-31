"""
Panel de ejecución paso a paso de recetas
Integra el selector de modo manual con la ejecución de procesos
"""

from nicegui import ui
from ui.state.app_state import app_state
from ui.styles.colors import COLORS, MODO_ICONOS, ESTADO_LED_COLORS
from ui.components.mode_selector import create_mode_selector, create_mode_validation_info, show_mode_mismatch_dialog
from ui.components.common import create_led_indicator, show_success_notification, show_error_notification, create_confirmation_dialog
from controllers.robot_controller import RobotController
from typing import Optional, Callable
import asyncio


class ExecutionPanel:
    """Panel de ejecución manual paso a paso de recetas"""

    def __init__(self, robot_ctrl: RobotController):
        """
        Args:
            robot_ctrl: Controlador del robot
        """
        self.robot_ctrl = robot_ctrl
        self.container = None
        self.step_container = None
        self.progress_bar = None
        self.progress_label = None
        self.execute_button = None

    def render(self):
        """Renderiza el panel completo"""
        if not app_state.receta_actual:
            return self._render_no_recipe()

        self.container = ui.column().classes('w-full h-full gap-6')

        with self.container:
            # Header con info de receta
            self._render_recipe_header()

            # Progreso general
            self._render_progress_overview()

            # Contenedor del paso actual
            self.step_container = ui.column().classes('w-full gap-6')
            with self.step_container:
                self._render_current_step()

            # Botones de control
            self._render_control_buttons()

        return self.container

    def _render_no_recipe(self):
        """Muestra mensaje cuando no hay receta cargada"""
        with ui.column().classes('w-full h-full items-center justify-center gap-6'):
            ui.icon('info').classes('text-8xl text-gray-400')
            ui.label('No hay receta cargada').classes(
                'text-3xl font-bold text-gray-600 dark:text-gray-400'
            )
            ui.label('Selecciona una receta del navegador para comenzar').classes(
                'text-lg text-gray-500 dark:text-gray-500'
            )

    def _render_recipe_header(self):
        """Header con información de la receta"""
        receta = app_state.receta_actual

        with ui.card().classes(
            'w-full bg-gradient-to-r from-thermo-cyan-500 to-blue-600 '
            'rounded-2xl p-6 shadow-2xl border-2 border-thermo-cyan-400'
        ):
            with ui.row().classes('w-full items-center justify-between'):
                # Icono + Nombre
                with ui.row().classes('items-center gap-4'):
                    ui.icon('restaurant_menu').classes('text-6xl text-white')
                    with ui.column().classes('gap-1'):
                        ui.label(receta.nombre).classes(
                            'text-4xl font-bold text-white'
                        )
                        if receta.descripcion:
                            ui.label(receta.descripcion).classes(
                                'text-lg text-white/80'
                            )

                # Stats
                with ui.column().classes('items-end gap-2'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('format_list_numbered').classes('text-white text-2xl')
                        ui.label(f'{receta.get_num_pasos()} pasos').classes(
                            'text-xl font-bold text-white'
                        )

                    with ui.row().classes('items-center gap-2'):
                        ui.icon('schedule').classes('text-white text-2xl')
                        duracion_min = receta.get_duracion_total() // 60
                        ui.label(f'{duracion_min} min').classes(
                            'text-xl font-bold text-white'
                        )

    def _render_progress_overview(self):
        """Barra de progreso general de la receta"""
        receta = app_state.receta_actual
        total_pasos = receta.get_num_pasos()
        paso_actual = app_state.paso_actual

        # Calcular porcentaje
        if app_state.paso_completado and paso_actual < total_pasos:
            # Si el paso está completado, contar como siguiente
            pasos_completados = paso_actual + 1
        else:
            pasos_completados = paso_actual

        porcentaje = int((pasos_completados / total_pasos) * 100)

        with ui.card().classes(
            'w-full bg-white dark:bg-gray-800 rounded-2xl p-6 '
            'border border-gray-200 dark:border-gray-700 shadow-lg'
        ):
            # Título
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Progreso General').classes(
                    'text-2xl font-bold text-gray-900 dark:text-white'
                )
                self.progress_label = ui.label(f'{pasos_completados}/{total_pasos} pasos completados').classes(
                    'text-lg font-semibold text-thermo-cyan-600 dark:text-thermo-cyan-400'
                )

            # Barra de progreso
            self.progress_bar = ui.linear_progress(
                value=porcentaje / 100,
                show_value=True
            ).props('size=30px color=cyan-6').classes('w-full')

            # Pasos completados (checkmarks)
            with ui.row().classes('w-full gap-2 mt-4 flex-wrap'):
                for i in range(total_pasos):
                    is_completed = i < pasos_completados
                    is_current = i == paso_actual and not app_state.paso_completado

                    step_classes = [
                        'flex items-center justify-center',
                        'w-10 h-10 rounded-full',
                        'font-bold text-sm'
                    ]

                    if is_current:
                        step_classes.extend([
                            'bg-thermo-cyan-500 text-white',
                            'ring-4 ring-thermo-cyan-300 dark:ring-thermo-cyan-700',
                            'animate-pulse-glow'
                        ])
                    elif is_completed:
                        step_classes.append('bg-green-500 text-white')
                    else:
                        step_classes.append('bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-400')

                    with ui.element('div').classes(' '.join(step_classes)):
                        if is_completed:
                            ui.icon('check').classes('text-xl')
                        else:
                            ui.label(str(i + 1))

    def _render_current_step(self):
        """Renderiza el paso actual con selector de modo"""
        receta = app_state.receta_actual
        paso_idx = app_state.paso_actual

        # Verificar si ya terminamos todos los pasos
        if paso_idx >= receta.get_num_pasos():
            self._render_completion_screen()
            return

        proceso = receta.procesos[paso_idx]

        with ui.card().classes(
            'w-full bg-white dark:bg-gray-800 rounded-3xl p-8 '
            'border-2 border-thermo-cyan-400 dark:border-thermo-cyan-600 shadow-2xl'
        ):
            # Badge del paso
            with ui.row().classes('items-center gap-4 mb-6'):
                with ui.element('div').classes(
                    'bg-thermo-cyan-500 text-white px-6 py-3 rounded-full font-bold text-2xl'
                ):
                    ui.label(f'PASO {paso_idx + 1} DE {receta.get_num_pasos()}')

            # Información del proceso
            with ui.column().classes('w-full gap-6 mb-8'):
                # Título con icono
                modo_proceso = proceso.__class__.__name__
                with ui.row().classes('items-center gap-4'):
                    ui.label(MODO_ICONOS.get(modo_proceso, '🔧')).classes('text-6xl')
                    with ui.column().classes('gap-2'):
                        ui.label(proceso.get_descripcion()).classes(
                            'text-3xl font-bold text-gray-900 dark:text-white'
                        )
                        ui.label(f'Modo recomendado: {modo_proceso}').classes(
                            'text-lg text-gray-600 dark:text-gray-400'
                        )

                # Detalles del paso
                with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 mt-4'):
                    # Duración
                    with ui.card().classes(
                        'bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4 '
                        'border border-blue-200 dark:border-blue-800'
                    ):
                        with ui.row().classes('items-center gap-3'):
                            ui.icon('schedule').classes('text-3xl text-blue-600 dark:text-blue-400')
                            with ui.column().classes('gap-1'):
                                ui.label('Duración').classes('text-sm text-gray-600 dark:text-gray-400')
                                ui.label(f'{proceso.get_duracion()} segundos').classes(
                                    'text-2xl font-bold text-gray-900 dark:text-white'
                                )

                    # Estado
                    with ui.card().classes(
                        'bg-green-50 dark:bg-green-900/20 rounded-xl p-4 '
                        'border border-green-200 dark:border-green-800'
                    ):
                        with ui.row().classes('items-center gap-3'):
                            estado_icon = 'check_circle' if app_state.paso_completado else 'pending'
                            estado_text = 'Completado' if app_state.paso_completado else 'Pendiente'
                            ui.icon(estado_icon).classes('text-3xl text-green-600 dark:text-green-400')
                            with ui.column().classes('gap-1'):
                                ui.label('Estado').classes('text-sm text-gray-600 dark:text-gray-400')
                                ui.label(estado_text).classes(
                                    'text-2xl font-bold text-gray-900 dark:text-white'
                                )

            ui.separator().classes('bg-gray-300 dark:bg-gray-700 my-6')

            # SELECTOR DE MODO (si el paso no está completado)
            if not app_state.paso_completado and not app_state.en_ejecucion:
                ui.label('Selecciona el Modo de Cocción').classes(
                    'text-2xl font-bold text-gray-900 dark:text-white mb-4'
                )

                create_mode_selector(on_select=self._on_mode_selected)

                # Validación visual
                create_mode_validation_info()

    def _render_completion_screen(self):
        """Pantalla de finalización de receta"""
        with ui.column().classes('w-full items-center justify-center gap-8 py-16'):
            # Animación de éxito
            ui.icon('check_circle').classes(
                'text-9xl text-green-500 animate-pulse-glow'
            )

            # Mensaje
            ui.label('¡Receta Completada!').classes(
                'text-5xl font-bold text-gray-900 dark:text-white'
            )

            ui.label(f'{app_state.receta_actual.nombre} está listo para servir').classes(
                'text-2xl text-gray-600 dark:text-gray-400'
            )

            # Stats finales
            with ui.card().classes(
                'bg-gradient-to-r from-green-50 to-cyan-50 '
                'dark:from-green-900/20 dark:to-cyan-900/20 '
                'rounded-2xl p-8 border-2 border-green-400 dark:border-green-600 mt-8'
            ):
                ui.label('Resumen de Ejecución').classes(
                    'text-2xl font-bold text-gray-900 dark:text-white mb-4'
                )

                with ui.grid().classes('grid-cols-3 gap-8'):
                    # Pasos completados
                    with ui.column().classes('items-center gap-2'):
                        ui.icon('format_list_numbered').classes('text-5xl text-green-600')
                        ui.label(str(app_state.receta_actual.get_num_pasos())).classes(
                            'text-4xl font-bold text-gray-900 dark:text-white'
                        )
                        ui.label('Pasos').classes('text-sm text-gray-600 dark:text-gray-400')

                    # Duración total
                    with ui.column().classes('items-center gap-2'):
                        ui.icon('schedule').classes('text-5xl text-blue-600')
                        duracion_min = app_state.receta_actual.get_duracion_total() // 60
                        ui.label(f'{duracion_min}m').classes(
                            'text-4xl font-bold text-gray-900 dark:text-white'
                        )
                        ui.label('Duración').classes('text-sm text-gray-600 dark:text-gray-400')

                    # Estado
                    with ui.column().classes('items-center gap-2'):
                        ui.icon('check_circle').classes('text-5xl text-green-600')
                        ui.label('100%').classes(
                            'text-4xl font-bold text-gray-900 dark:text-white'
                        )
                        ui.label('Completado').classes('text-sm text-gray-600 dark:text-gray-400')

            # Botón finalizar
            ui.button(
                'Finalizar y Volver',
                icon='home',
                on_click=self._finish_execution
            ).props('unelevated size=xl').classes(
                'bg-thermo-cyan-500 hover:bg-thermo-cyan-600 '
                'text-white px-12 py-4 rounded-2xl font-bold text-xl mt-8'
            )

    def _render_control_buttons(self):
        """Botones de control de ejecución"""
        if app_state.paso_actual >= app_state.receta_actual.get_num_pasos():
            return  # Ya terminamos

        with ui.row().classes('w-full justify-between items-center mt-8'):
            # Botón Detener
            ui.button(
                'Detener Receta',
                icon='stop_circle',
                on_click=self._stop_execution
            ).props('outline color=red').classes(
                'px-8 py-3 rounded-xl font-semibold'
            )

            # Botón Ejecutar / Siguiente
            if app_state.paso_completado:
                # Paso completado, mostrar "Siguiente"
                ui.button(
                    'Siguiente Paso',
                    icon='arrow_forward',
                    on_click=self._next_step
                ).props('unelevated').classes(
                    'bg-thermo-cyan-500 hover:bg-thermo-cyan-600 '
                    'text-white px-12 py-4 rounded-xl font-bold text-lg'
                )
            else:
                # Mostrar "Ejecutar"
                modo_seleccionado = app_state.modo_seleccionado
                puede_ejecutar = modo_seleccionado is not None and not app_state.en_ejecucion

                self.execute_button = ui.button(
                    'Ejecutar Paso',
                    icon='play_arrow',
                    on_click=self._execute_step
                ).props('unelevated' if puede_ejecutar else 'disable').classes(
                    'bg-green-500 hover:bg-green-600 '
                    'text-white px-12 py-4 rounded-xl font-bold text-lg'
                )

    def _on_mode_selected(self, modo: str):
        """Callback cuando se selecciona un modo"""
        print(f"[EXECUTION] Modo seleccionado: {modo}")

        # Si hay botón de ejecutar, habilitarlo
        if self.execute_button:
            self.execute_button.props(remove='disable')
            self.execute_button.props(add='unelevated')
            self.execute_button.update()

    def _execute_step(self):
        """Ejecuta el paso actual con el modo seleccionado"""
        if not app_state.modo_seleccionado:
            show_error_notification('⚠️ Debes seleccionar un modo de cocción')
            return

        receta = app_state.receta_actual
        proceso = receta.procesos[app_state.paso_actual]
        modo_proceso = proceso.__class__.__name__
        modo_usuario = app_state.modo_seleccionado

        # Verificar si el modo coincide con la receta
        if modo_usuario != modo_proceso:
            # Mostrar diálogo de advertencia
            def on_confirm():
                self._do_execute_step()

            show_mode_mismatch_dialog(modo_usuario, modo_proceso, on_confirm)
        else:
            # Ejecutar directamente
            self._do_execute_step()

    def _do_execute_step(self):
        """Ejecuta el paso realmente"""
        app_state.en_ejecucion = True

        # Deshabilitar botón
        if self.execute_button:
            self.execute_button.props(add='disable')
            self.execute_button.props(add='loading')
            self.execute_button.update()

        # Ejecutar proceso
        receta = app_state.receta_actual
        proceso = receta.procesos[app_state.paso_actual]

        # Callback de log
        def log_callback(msg: str):
            print(f"[PROCESO] {msg}")

        # Ejecutar
        exito = proceso.ejecutar(log_callback)

        # Marcar como completado
        app_state.paso_completado = True
        app_state.en_ejecucion = False

        # Notificar
        if exito:
            show_success_notification(f'✓ Paso {app_state.paso_actual + 1} completado')
        else:
            show_error_notification('❌ Error al ejecutar el paso')

        # Refrescar vista
        self._refresh_view()

    def _next_step(self):
        """Avanza al siguiente paso"""
        app_state.siguiente_paso()

        # Refrescar vista
        self._refresh_view()

    def _stop_execution(self):
        """Detiene la ejecución de la receta"""
        def on_confirm():
            app_state.reset_execution()
            show_success_notification('Ejecución detenida')
            self._refresh_view()

        create_confirmation_dialog(
            title='¿Detener Receta?',
            message='Se perderá el progreso actual. ¿Estás seguro?',
            on_confirm=on_confirm,
            confirm_text='Sí, Detener',
            cancel_text='Cancelar'
        )

    def _finish_execution(self):
        """Finaliza y vuelve al inicio"""
        app_state.reset_execution()
        ui.notify('Receta finalizada', type='positive', position='top')
        # Aquí se podría navegar a otra vista

    def _refresh_view(self):
        """Refresca la vista del panel"""
        if self.container:
            self.container.clear()
            with self.container:
                if not app_state.receta_actual:
                    self._render_no_recipe()
                else:
                    self._render_recipe_header()
                    self._render_progress_overview()

                    self.step_container = ui.column().classes('w-full gap-6')
                    with self.step_container:
                        self._render_current_step()

                    self._render_control_buttons()


# ===== FUNCIÓN HELPER =====
def create_execution_panel(robot_ctrl: RobotController):
    """
    Crea el panel de ejecución

    Args:
        robot_ctrl: Controlador del robot

    Returns:
        ExecutionPanel instance
    """
    panel = ExecutionPanel(robot_ctrl)
    return panel.render()
