"""
Navegador de recetas con grid view, filtros y búsqueda
Permite explorar recetas preinstaladas y personalizadas
"""

from nicegui import ui
from ui.state.app_state import app_state
from ui.styles.colors import COLORS, MODO_ICONOS
from controllers.recetas_controller import RecetasController
from typing import List, Optional
from models.receta import Receta


class RecipeBrowser:
    """Componente de navegación y exploración de recetas"""

    def __init__(self, recetas_ctrl: RecetasController):
        self.recetas_ctrl = recetas_ctrl
        self.container = None
        self.grid_container = None
        self.search_input = None

    def render(self):
        """Renderiza el navegador completo"""
        self.container = ui.column().classes('w-full gap-6 p-6')

        with self.container:
            # Header con título y acciones
            self._render_header()

            # Barra de filtros y búsqueda
            self._render_filter_bar()

            # Grid de recetas
            self._render_recipe_grid()

        return self.container

    def _render_header(self):
        """Header con título y botón de crear receta"""
        with ui.row().classes('w-full items-center justify-between mb-4'):
            # Título
            with ui.row().classes('items-center gap-3'):
                ui.icon('restaurant_menu').classes('text-5xl text-thermo-cyan-500')
                ui.label('Biblioteca de Recetas').classes(
                    'text-4xl font-bold text-thermo-navy-700 dark:text-white'
                )

            # Botón crear nueva receta
            ui.button(
                'Nueva Receta',
                icon='add_circle',
                on_click=self._open_create_wizard
            ).props('unelevated').classes(
                'bg-thermo-cyan-500 hover:bg-thermo-cyan-600 '
                'text-white px-6 py-3 rounded-xl font-semibold '
                'shadow-lg hover:shadow-glow-cyan transition-all'
            )

    def _render_filter_bar(self):
        """Barra de filtros y búsqueda"""
        with ui.card().classes(
            'w-full bg-white dark:bg-gray-800 rounded-2xl p-4 '
            'border border-gray-200 dark:border-gray-700'
        ):
            with ui.row().classes('w-full items-center gap-4 flex-wrap'):
                # Filtros de tipo
                with ui.row().classes('items-center gap-2'):
                    ui.label('Filtrar:').classes(
                        'text-sm font-semibold text-gray-600 dark:text-gray-400'
                    )

                    # Toggle de filtros
                    filtros = {
                        'todas': '📚 Todas',
                        'base': '⭐ Preinstaladas',
                        'usuario': '👤 Mis Recetas',
                        'favoritas': '⭐ Favoritas'
                    }

                    for key, label in filtros.items():
                        self._create_filter_button(key, label)

                ui.space()

                # Barra de búsqueda
                self.search_input = ui.input(
                    placeholder='Buscar recetas...'
                ).props('outlined dense').classes(
                    'w-64'
                ).on('input', lambda: self._refresh_grid())

                self.search_input._props['prepend-icon'] = 'search'

    def _create_filter_button(self, filter_key: str, label: str):
        """Crea un botón de filtro"""
        is_active = app_state.filtro_recetas == filter_key

        btn = ui.button(
            label,
            on_click=lambda: self._set_filter(filter_key)
        ).props('dense')

        if is_active:
            btn.classes(
                'bg-thermo-cyan-500 text-white font-semibold px-4 py-2 rounded-lg'
            )
        else:
            btn.props('outline').classes(
                'text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg '
                'hover:bg-thermo-cyan-50 dark:hover:bg-thermo-cyan-900/20'
            )

    def _set_filter(self, filter_key: str):
        """Cambia el filtro activo"""
        app_state.filtro_recetas = filter_key
        self._refresh_grid()
        ui.notify(f'Mostrando: {filter_key}', type='info', position='top')

    def _render_recipe_grid(self):
        """Grid responsivo de tarjetas de recetas"""
        self.grid_container = ui.column().classes('w-full gap-4')

        with self.grid_container:
            # Obtener recetas filtradas
            recetas = self._get_filtered_recipes()

            if not recetas:
                # Sin resultados
                self._render_empty_state()
            else:
                # Contador de resultados
                ui.label(f'{len(recetas)} receta(s) encontrada(s)').classes(
                    'text-sm text-gray-600 dark:text-gray-400 mb-2'
                )

                # Grid responsive
                with ui.grid().classes(
                    'w-full gap-6 '
                    'grid-cols-1 '           # Mobile
                    'sm:grid-cols-2 '        # Tablet
                    'lg:grid-cols-3 '        # Desktop
                    'xl:grid-cols-4'         # Large desktop
                ):
                    for receta in recetas:
                        self._render_recipe_card(receta)

    def _render_recipe_card(self, receta: Receta):
        """Renderiza una tarjeta individual de receta"""
        with ui.card().classes(
            'relative bg-white dark:bg-gray-800 rounded-2xl '
            'border-2 border-gray-200 dark:border-gray-700 '
            'hover:border-thermo-cyan-400 dark:hover:border-thermo-cyan-600 '
            'hover:shadow-xl hover:-translate-y-2 '
            'transition-all duration-300 cursor-pointer '
            'overflow-hidden'
        ).on('click', lambda r=receta: self._load_recipe(r)):

            # Badge de tipo (esquina superior derecha)
            with ui.element('div').classes(
                'absolute top-3 right-3 z-10'
            ):
                badge_icon = '⭐' if receta.es_base else '👤'
                badge_color = 'bg-yellow-500' if receta.es_base else 'bg-thermo-cyan-500'
                with ui.element('div').classes(
                    f'{badge_color} text-white px-3 py-1 rounded-full '
                    'text-xs font-bold shadow-lg'
                ):
                    ui.label(badge_icon)

            # Botón de favorito (solo para recetas de usuario)
            if not receta.es_base:
                is_fav = getattr(receta, 'favorito', False)
                fav_icon = 'star' if is_fav else 'star_border'
                fav_color = 'text-yellow-500' if is_fav else 'text-gray-400'

                ui.button(
                    icon=fav_icon,
                    on_click=lambda r=receta: self._toggle_favorite(r)
                ).props('flat round dense').classes(
                    f'absolute top-3 left-3 z-10 {fav_color} hover:text-yellow-500 transition-colors bg-white/80'
                )

            # Contenido de la card
            with ui.column().classes('w-full gap-3 p-6'):
                # Título
                ui.label(receta.nombre).classes(
                    'text-xl font-bold text-gray-900 dark:text-white line-clamp-2'
                )

                # Descripción
                if receta.descripcion:
                    ui.label(receta.descripcion).classes(
                        'text-sm text-gray-600 dark:text-gray-400 line-clamp-2'
                    )

                # Separador
                ui.separator().classes('bg-gray-200 dark:bg-gray-700')

                # Stats
                with ui.row().classes('w-full items-center gap-4 flex-wrap'):
                    # Número de pasos
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('format_list_numbered').classes('text-gray-500 text-sm')
                        ui.label(f'{receta.get_num_pasos()} pasos').classes(
                            'text-sm text-gray-700 dark:text-gray-300 font-medium'
                        )

                    # Duración total
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('schedule').classes('text-gray-500 text-sm')
                        duracion_min = receta.get_duracion_total() // 60
                        duracion_seg = receta.get_duracion_total() % 60
                        duracion_text = f'{duracion_min}m' if duracion_seg == 0 else f'{duracion_min}m {duracion_seg}s'
                        ui.label(duracion_text).classes(
                            'text-sm text-gray-700 dark:text-gray-300 font-medium'
                        )

                # Preview de procesos (iconos)
                if receta.procesos:
                    with ui.row().classes('w-full gap-1 flex-wrap mt-2'):
                        # Mostrar máximo 5 iconos
                        for proceso in receta.procesos[:5]:
                            tipo = proceso.__class__.__name__
                            icono = MODO_ICONOS.get(tipo, '🔧')
                            ui.label(icono).classes('text-lg').tooltip(tipo)

                        # Indicador de "más procesos"
                        if len(receta.procesos) > 5:
                            ui.label(f'+{len(receta.procesos) - 5}').classes(
                                'text-xs text-gray-500 dark:text-gray-400 font-medium'
                            )

                # Botón de acción
                ui.button(
                    'Cocinar',
                    icon='play_arrow',
                    on_click=lambda r=receta: self._load_recipe(r)
                ).props('unelevated').classes(
                    'w-full bg-thermo-cyan-500 hover:bg-thermo-cyan-600 '
                    'text-white font-semibold py-2 rounded-xl mt-2'
                )

    def _render_empty_state(self):
        """Muestra mensaje cuando no hay recetas"""
        with ui.column().classes('w-full items-center justify-center py-16 gap-4'):
            ui.icon('search_off').classes('text-8xl text-gray-400')
            ui.label('No se encontraron recetas').classes(
                'text-2xl font-bold text-gray-600 dark:text-gray-400'
            )

            filtro = app_state.filtro_recetas
            if filtro == 'favoritas':
                ui.label('Marca algunas recetas como favoritas para verlas aquí').classes(
                    'text-gray-500 dark:text-gray-500'
                )
            elif filtro == 'usuario':
                ui.label('Crea tu primera receta personalizada').classes(
                    'text-gray-500 dark:text-gray-500'
                )
                ui.button(
                    'Crear Receta',
                    icon='add_circle',
                    on_click=self._open_create_wizard
                ).props('unelevated color=cyan-6').classes('mt-4')

    def _get_filtered_recipes(self) -> List[Receta]:
        """Obtiene las recetas según el filtro activo"""
        # Obtener todas las recetas
        recetas_base, recetas_usuario = self.recetas_ctrl.obtener_todas_recetas()

        # Aplicar filtro
        filtro = app_state.filtro_recetas

        if filtro == 'base':
            recetas = recetas_base
        elif filtro == 'usuario':
            recetas = recetas_usuario
        elif filtro == 'favoritas':
            # Solo recetas de usuario favoritas
            recetas = [r for r in recetas_usuario if getattr(r, 'favorito', False)]
        else:  # 'todas'
            recetas = recetas_base + recetas_usuario

        # Aplicar búsqueda
        if self.search_input and self.search_input.value:
            search_term = self.search_input.value.lower()
            recetas = [
                r for r in recetas
                if search_term in r.nombre.lower() or
                   (r.descripcion and search_term in r.descripcion.lower())
            ]

        # Ordenar: favoritas primero, luego alfabético
        recetas.sort(key=lambda r: (
            not getattr(r, 'favorito', False),  # Favoritas primero
            r.nombre.lower()  # Luego alfabético
        ))

        return recetas

    def _refresh_grid(self):
        """Refresca el grid de recetas"""
        if self.grid_container:
            self.grid_container.clear()
            with self.grid_container:
                recetas = self._get_filtered_recipes()

                if not recetas:
                    self._render_empty_state()
                else:
                    ui.label(f'{len(recetas)} receta(s) encontrada(s)').classes(
                        'text-sm text-gray-600 dark:text-gray-400 mb-2'
                    )

                    with ui.grid().classes(
                        'w-full gap-6 '
                        'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
                    ):
                        for receta in recetas:
                            self._render_recipe_card(receta)

    def _load_recipe(self, receta: Receta):
        """Carga una receta para ejecutar"""
        app_state.cargar_receta(receta)
        ui.notify(f'✓ Receta cargada: {receta.nombre}', type='positive', position='top')
        # Aquí cambiaríamos a la vista de ejecución
        # Por ahora solo actualizamos el estado

    def _toggle_favorite(self, receta: Receta):
        """Toggle favorito de una receta"""
        if receta.es_base:
            ui.notify('⚠️ No puedes marcar recetas preinstaladas como favoritas', type='warning')
            return

        try:
            # Actualizar en BD
            nuevo_estado = self.recetas_ctrl.toggle_favorito(receta.id, receta.es_base)

            # Actualizar en modelo
            receta.favorito = nuevo_estado

            # Notificar
            msg = '⭐ Agregada a favoritos' if nuevo_estado else 'Eliminada de favoritos'
            ui.notify(msg, type='positive', position='top')

            # Refrescar grid si estamos en vista de favoritas
            if app_state.filtro_recetas == 'favoritas':
                self._refresh_grid()

        except Exception as e:
            ui.notify(f'❌ Error: {str(e)}', type='negative')

    def _open_create_wizard(self):
        """Abre el wizard de creación de recetas"""
        app_state.vista_actual = 'wizard'
        ui.notify('📝 Abriendo wizard de creación...', type='info')
        # Aquí se cambiaría a la vista del wizard


def create_recipe_browser(recetas_ctrl: RecetasController):
    """
    Función helper para crear el navegador de recetas

    Args:
        recetas_ctrl: Controlador de recetas

    Returns:
        RecipeBrowser instance
    """
    browser = RecipeBrowser(recetas_ctrl)
    return browser.render()
