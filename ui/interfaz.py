"""
Interfaz gráfica del Robot de Cocina usando NiceGUI
Diseño tipo Thermomix con BOTÓN ÚNICO CONTEXTUAL
Sistema 100% MANUAL - Paso a paso
VERSIÓN PROFESIONAL - Bug de detención CORREGIDO
"""
from nicegui import ui, app
from controllers.robot_controller import RobotController
from controllers.recetas_controller import RecetasController
from main import (
    ESTADO_APAGADO, ESTADO_ENCENDIDO,
    ESTADO_EJECUTANDO, ESTADO_DETENIDO,
    COLOR_APAGADO, COLOR_ENCENDIDO,
    COLOR_EJECUTANDO, COLOR_DETENIDO
)

# Controladores globales
robot_ctrl = RobotController()
recetas_ctrl = RecetasController()

# Referencias a elementos UI
estado_led = None
estado_texto = None
pantalla_paso = None
pantalla_info = None
barra_progreso = None
label_progreso = None
log_area = None
boton_accion_principal = None
label_accion = None
boton_anterior = None

# Estado de la receta actual
receta_actual = None
paso_actual = 0
en_ejecucion = False
paso_completado = False

def agregar_log(mensaje: str):
    """Agrega un mensaje al log"""
    if log_area:
        valor_actual = log_area.value
        lineas = valor_actual.split('\n')
        lineas.append(mensaje)
        if len(lineas) > 15:
            lineas = lineas[-15:]
        log_area.value = '\n'.join(lineas)

def actualizar_estado_ui(estado: str):
    """Actualiza los elementos UI según el estado"""
    actualizar_boton_accion()

def actualizar_progreso(paso_num: int, total_pasos: int):
    """Actualiza la barra de progreso"""
    if barra_progreso and label_progreso:
        if total_pasos > 0:
            progreso = paso_num / total_pasos
            barra_progreso.value = round(progreso, 2)
        label_progreso.text = f'{paso_num}/{total_pasos}'
        barra_progreso.update()
        label_progreso.update()

def actualizar_pantalla_estado(estado: str, mensaje: str = ''):
    """Actualiza la pantalla principal con el estado"""
    if estado_led:
        colores = {
            ESTADO_APAGADO: 'background: #dc2626; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);',
            ESTADO_ENCENDIDO: 'background: #16a34a; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);',
            ESTADO_EJECUTANDO: 'background: #2563eb; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);',
            ESTADO_DETENIDO: 'background: #ea580c; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);'
        }
        estado_led.style(f'width: 24px; height: 24px; border-radius: 50%; {colores.get(estado, "background: #6b7280;")}')
    
    if estado_texto:
        textos = {
            ESTADO_APAGADO: 'APAGADO',
            ESTADO_ENCENDIDO: 'LISTO',
            ESTADO_EJECUTANDO: 'EJECUTANDO',
            ESTADO_DETENIDO: 'PAUSADO'
        }
        estado_texto.text = textos.get(estado, 'DESCONOCIDO')
    
    if pantalla_info and mensaje:
        pantalla_info.text = mensaje

def actualizar_pantalla_paso():
    """Actualiza la pantalla con el paso actual"""
    global receta_actual, paso_actual
    
    if not receta_actual:
        if pantalla_paso:
            pantalla_paso.text = 'No hay receta cargada'
        if pantalla_info:
            pantalla_info.text = 'Selecciona una receta para comenzar'
        actualizar_boton_accion()
        return
    
    total = receta_actual.get_num_pasos()
    
    if paso_actual >= total:
        if pantalla_paso:
            pantalla_paso.text = '¡RECETA COMPLETADA!'
        if pantalla_info:
            pantalla_info.text = f'{receta_actual.nombre} terminada con éxito'
        actualizar_progreso(total, total)
        actualizar_boton_accion()
        return
    
    proceso = receta_actual.procesos[paso_actual]
    
    if pantalla_paso:
        pantalla_paso.text = f'PASO {paso_actual + 1}/{total}'
    
    if pantalla_info:
        info = f'{proceso.get_descripcion()}\n'
        info += f'Duración: {proceso.get_duracion()}s'
        if proceso.parametros:
            info += f'\nParámetros: {proceso.parametros}'
        pantalla_info.text = info
    
    actualizar_progreso(paso_actual, total)
    
    if boton_anterior:
        boton_anterior.enabled = paso_actual > 0
    
    actualizar_boton_accion()

def actualizar_boton_accion():
    """Actualiza el botón de acción principal según el contexto"""
    global boton_accion_principal, label_accion, en_ejecucion, paso_completado, receta_actual, paso_actual
    
    if not boton_accion_principal or not label_accion:
        return
    
    # Estado: Robot apagado o sin receta
    if not robot_ctrl.esta_encendido or not receta_actual:
        boton_accion_principal.enabled = False
        boton_accion_principal._props['icon'] = 'power_off'
        boton_accion_principal.style(
            'width: 140px; height: 140px; background: #6b7280; '
            'box-shadow: 0 8px 0 #6b7280dd, 0 12px 24px rgba(0,0,0,0.4); opacity: 0.5;'
        )
        label_accion.text = 'SIN RECETA'
        label_accion.update()
        boton_accion_principal.update()
        return
    
    # Receta completada
    if paso_actual >= receta_actual.get_num_pasos():
        boton_accion_principal.enabled = False
        boton_accion_principal._props['icon'] = 'check_circle'
        boton_accion_principal.style(
            'width: 140px; height: 140px; background: #10b981; '
            'box-shadow: 0 8px 0 #10b981dd, 0 12px 24px rgba(0,0,0,0.4); opacity: 0.7;'
        )
        label_accion.text = 'TERMINADO'
        label_accion.update()
        boton_accion_principal.update()
        return
    
    # Estado: Ejecutando
    if en_ejecucion:
        boton_accion_principal.enabled = True
        boton_accion_principal._props['icon'] = 'stop'
        boton_accion_principal.style(
            'width: 140px; height: 140px; background: #ef4444; '
            'box-shadow: 0 8px 0 #ef4444dd, 0 12px 24px rgba(0,0,0,0.4);'
        )
        label_accion.text = 'DETENER'
        label_accion.update()
        boton_accion_principal.update()
        return
    
    # Estado: Paso completado
    if paso_completado:
        boton_accion_principal.enabled = True
        boton_accion_principal._props['icon'] = 'arrow_forward'
        boton_accion_principal.style(
            'width: 140px; height: 140px; background: #3b82f6; '
            'box-shadow: 0 8px 0 #3b82f6dd, 0 12px 24px rgba(0,0,0,0.4); '
            'animation: pulse 1.5s ease-in-out infinite;'
        )
        label_accion.text = 'SIGUIENTE'
        label_accion.update()
        boton_accion_principal.update()
        return
    
    # Estado: Listo para ejecutar
    boton_accion_principal.enabled = True
    boton_accion_principal._props['icon'] = 'play_arrow'
    boton_accion_principal.style(
        'width: 140px; height: 140px; background: #8b5cf6; '
        'box-shadow: 0 8px 0 #8b5cf6dd, 0 12px 24px rgba(0,0,0,0.4); opacity: 1;'
    )
    label_accion.text = 'COCINAR'
    label_accion.update()
    boton_accion_principal.update()

def accion_principal_click():
    """Handler único que decide qué hacer según el estado actual"""
    global en_ejecucion, paso_completado, receta_actual, paso_actual
    
    if en_ejecucion:
        on_parar()
        return
    
    if paso_completado:
        siguiente_paso()
        return
    
    ejecutar_paso_actual()

def on_encender():
    """Handler para encender el robot"""
    robot_ctrl.encender()
    actualizar_pantalla_estado(ESTADO_ENCENDIDO, 'Sistema listo')
    actualizar_boton_accion()
    ui.notify('Robot encendido', type='positive')

def on_apagar():
    """Handler para apagar el robot"""
    global receta_actual, paso_actual, paso_completado
    robot_ctrl.apagar()
    receta_actual = None
    paso_actual = 0
    paso_completado = False
    actualizar_pantalla_estado(ESTADO_APAGADO, 'Sistema apagado')
    actualizar_pantalla_paso()
    if barra_progreso:
        barra_progreso.value = 0
    if label_progreso:
        label_progreso.text = '0/0'
    actualizar_boton_accion()
    ui.notify('Robot apagado', type='warning')

def on_parar():
    """Handler para parar ejecución - CORREGIDO"""
    global paso_completado, en_ejecucion
    
    # ⭐ CORRECCIÓN: Resetear flags correctamente ⭐
    en_ejecucion = False
    paso_completado = False
    
    robot_ctrl.parar()
    actualizar_pantalla_estado(ESTADO_DETENIDO, 'Paso interrumpido')
    actualizar_boton_accion()
    ui.notify('Ejecución detenida', type='warning')

def seleccionar_receta():
    """Muestra el menú de selección de recetas - PROFESIONAL"""
    if not robot_ctrl.esta_encendido:
        ui.notify('Enciende el robot primero', type='warning')
        return
    
    base, usuario = recetas_ctrl.obtener_todas_recetas()
    opciones_base = {r.id: f"{r.nombre} ({r.get_num_pasos()} pasos · {r.get_duracion_total()}s)" for r in base}
    opciones_usuario = {r.id: f"{r.nombre} ({r.get_num_pasos()} pasos · {r.get_duracion_total()}s)" for r in usuario}
    
    selector = None
    tipo_selector = None
    
    def confirmar():
        global receta_actual, paso_actual, paso_completado
        
        if not selector.value or not tipo_selector.value:
            ui.notify('Selecciona una receta', type='warning')
            return
        
        es_base = (tipo_selector.value == 'base')
        receta_actual = recetas_ctrl.obtener_receta_por_id(selector.value, es_base)
        
        if receta_actual:
            paso_actual = 0
            paso_completado = False
            actualizar_pantalla_paso()
            actualizar_pantalla_estado(ESTADO_ENCENDIDO, f'{receta_actual.nombre} cargada')
            ui.notify(f'Receta cargada: {receta_actual.nombre}', type='positive')
            dialog.close()
    
    def cambiar_tipo(e):
        if e.value == 'base':
            selector.options = opciones_base
        else:
            selector.options = opciones_usuario
        selector.value = None
        selector.update()
    
    # DIÁLOGO PROFESIONAL
    with ui.dialog() as dialog, ui.card().style(
        'background: linear-gradient(145deg, #1e293b, #0f172a); '
        'border: 2px solid #334155; '
        'border-radius: 20px; '
        'padding: 2.5rem; '
        'min-width: 550px; '
        'max-width: 650px; '
        'box-shadow: 0 20px 40px rgba(0,0,0,0.6);'
    ):
        # Título
        ui.label('SELECCIONAR RECETA').style(
            'font-size: 2rem; '
            'font-weight: bold; '
            'text-align: center; '
            'color: #e2e8f0; '
            'margin-bottom: 2.5rem; '
            'text-shadow: 0 2px 4px rgba(0,0,0,0.3);'
        )
        
        # TOGGLE MEJORADO
        with ui.column().classes('w-full items-center mb-6'):
            ui.label('TIPO DE RECETA').style(
                'font-size: 0.9rem; '
                'font-weight: 600; '
                'color: #94a3b8; '
                'margin-bottom: 1rem; '
                'letter-spacing: 1px;'
            )
            
            tipo_selector = ui.toggle(
                {
                    'base': 'PREINSTALADAS',
                    'usuario': 'MIS RECETAS'
                },
                value='base',
                on_change=cambiar_tipo
            ).props('color=blue-6 size=xl spread').style(
                'width: 100%; '
                'font-size: 1.1rem; '
                'font-weight: 600; '
                'padding: 0.8rem;'
            )
        
        # Selector de receta
        selector = ui.select(
            opciones_base,
            label='Selecciona una receta'
        ).props('outlined bg-color=blue-grey-9 label-color=blue-2').style(
            'width: 100%; '
            'margin-bottom: 2rem; '
            'font-size: 1.05rem;'
        )
        
        # Separador
        ui.separator().style('background: #475569; margin: 1.5rem 0;')
        
        # Botones
        with ui.row().classes('w-full justify-end gap-4'):
            ui.button('Cancelar', on_click=dialog.close).props(
                'outline color=red-6 size=lg'
            ).style(
                'font-weight: 600; '
                'padding: 0.7rem 2rem; '
                'border-radius: 10px;'
            )
            ui.button('Cargar Receta', on_click=confirmar).props(
                'color=green-6 size=lg'
            ).style(
                'font-weight: 600; '
                'padding: 0.7rem 2rem; '
                'border-radius: 10px;'
            )
    
    dialog.open()

def ejecutar_paso_actual():
    """Ejecuta el paso actual - CORREGIDO"""
    global receta_actual, paso_actual, en_ejecucion, paso_completado
    
    if not receta_actual or paso_actual >= receta_actual.get_num_pasos():
        ui.notify('No hay paso para ejecutar', type='warning')
        return
    
    # ⭐ CORRECCIÓN: Resetear flags ANTES de empezar ⭐
    paso_completado = False
    en_ejecucion = True
    
    proceso = receta_actual.procesos[paso_actual]
    actualizar_pantalla_estado(ESTADO_EJECUTANDO, f'Ejecutando paso {paso_actual + 1}...')
    actualizar_boton_accion()
    
    import threading
    import time
    stop_progress = {'value': False}
    
    def actualizar_progreso_proceso():
        tiempo_inicio = time.time()
        duracion = proceso.get_duracion()
        total = receta_actual.get_num_pasos()
        
        while not stop_progress['value']:
            tiempo_transcurrido = time.time() - tiempo_inicio
            if duracion > 0:
                progreso_paso = min(tiempo_transcurrido / duracion, 1.0)
                progreso_total = (paso_actual + progreso_paso) / total
                if barra_progreso:
                    barra_progreso.value = round(progreso_total, 2)
                    barra_progreso.update()
            time.sleep(0.3)
    
    thread_progreso = threading.Thread(target=actualizar_progreso_proceso, daemon=True)
    thread_progreso.start()
    
    def on_completado(exito):
        global en_ejecucion, paso_completado
        stop_progress['value'] = True
        en_ejecucion = False
        
        if exito:
            paso_completado = True
            actualizar_pantalla_estado(ESTADO_ENCENDIDO, f'Paso {paso_actual + 1} completado')
            actualizar_boton_accion()
            ui.notify(f'Paso {paso_actual + 1} completado', type='positive')
        else:
            paso_completado = False
            actualizar_pantalla_estado(ESTADO_DETENIDO, 'Paso interrumpido')
            actualizar_boton_accion()
            ui.notify('Paso interrumpido', type='warning')
    
    robot_ctrl.ejecutar_proceso_async(proceso, on_completado)

def siguiente_paso():
    """Avanza al siguiente paso"""
    global paso_actual, receta_actual, paso_completado
    
    if not receta_actual:
        ui.notify('Carga una receta primero', type='warning')
        return
    
    if paso_actual < receta_actual.get_num_pasos():
        paso_actual += 1
        paso_completado = False
        actualizar_pantalla_paso()
        if paso_actual < receta_actual.get_num_pasos():
            ui.notify(f'Paso {paso_actual + 1}', type='info')
        else:
            ui.notify('Receta completada', type='positive')

def anterior_paso():
    """Retrocede al paso anterior"""
    global paso_actual, paso_completado
    
    if paso_actual > 0:
        paso_actual -= 1
        paso_completado = False
        actualizar_pantalla_paso()
        ui.notify(f'Paso {paso_actual + 1}', type='info')
    else:
        ui.notify('Ya estás en el primer paso', type='info')

# ========== CONTINUACIÓN PARTE 2/3 ==========

def mostrar_menu_crear_receta():
    """Muestra el menú de creación de recetas - PROFESIONAL"""
    nombre_input = None
    desc_input = None
    pasos_list = None
    pasos_temporales = []
    
    def agregar_paso():
        paso_num = len(pasos_temporales) + 1
        tipos = recetas_ctrl.obtener_tipos_procesos_disponibles()
        
        paso_data = {'num': paso_num, 'tipo': None, 'params': '', 'duracion': 5}
        pasos_temporales.append(paso_data)
        
        with pasos_list:
            with ui.card().style(
                'background: #1e293b; '
                'border: 2px solid #475569; '
                'border-radius: 12px; '
                'padding: 1.5rem; '
                'margin-bottom: 1rem; '
                'box-shadow: 0 4px 8px rgba(0,0,0,0.3);'
            ) as card:
                with ui.row().classes('w-full items-center mb-3'):
                    ui.label(f'PASO {paso_num}').style(
                        'font-size: 1.2rem; '
                        'font-weight: bold; '
                        'color: #93c5fd;'
                    )
                    ui.space()
                    ui.button(icon='delete', on_click=lambda d=paso_data, c=card: eliminar_paso(d, c)).props(
                        'flat round dense color=red-6'
                    ).style('font-size: 1.2rem;')
                
                with ui.grid(columns=2).classes('w-full gap-4'):
                    tipo = ui.select(tipos, label='Tipo de Proceso').props(
                        'outlined bg-color=blue-grey-9 label-color=blue-2'
                    ).classes('col-span-1').style('color: #e2e8f0;')
                    
                    duracion = ui.number('Duración (segundos)', value=5, min=1, max=3600).props(
                        'outlined bg-color=blue-grey-9 label-color=blue-2'
                    ).classes('col-span-1').style('color: #e2e8f0;')
                    
                    params = ui.input('Parámetros', placeholder='Ej: ingrediente=harina, peso=250g').props(
                        'outlined bg-color=blue-grey-9 label-color=blue-2'
                    ).classes('col-span-2').style('color: #e2e8f0;')
                
                paso_data['tipo'] = tipo
                paso_data['params'] = params
                paso_data['duracion'] = duracion
    
    def eliminar_paso(paso_data, card):
        if len(pasos_temporales) <= 1:
            ui.notify('Debe haber al menos 1 paso', type='warning')
            return
        pasos_temporales.remove(paso_data)
        card.delete()
    
    def guardar():
        nombre = nombre_input.value.strip()
        desc = desc_input.value.strip()
        
        if not nombre:
            ui.notify('El nombre es obligatorio', type='warning')
            return
        
        if not pasos_temporales:
            ui.notify('Agrega al menos un paso', type='warning')
            return
        
        for i, paso in enumerate(pasos_temporales, 1):
            if not paso['tipo'].value:
                ui.notify(f'Selecciona el tipo para el Paso {i}', type='warning')
                return
        
        try:
            receta_id = recetas_ctrl.crear_receta_usuario(nombre, desc)
            
            for paso in pasos_temporales:
                recetas_ctrl.agregar_proceso_a_receta(
                    receta_id,
                    paso['tipo'].value,
                    paso['params'].value.strip(),
                    int(paso['duracion'].value)
                )
            
            ui.notify(f'Receta creada: {nombre}', type='positive')
            dialog.close()
            
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
    
    # DIÁLOGO PROFESIONAL
    with ui.dialog() as dialog, ui.card().style(
        'background: linear-gradient(145deg, #1e293b, #0f172a); '
        'border: 2px solid #334155; '
        'border-radius: 20px; '
        'padding: 2.5rem; '
        'min-width: 700px; '
        'max-width: 900px; '
        'max-height: 85vh; '
        'overflow-y: auto; '
        'box-shadow: 0 20px 40px rgba(0,0,0,0.6);'
    ):
        # Título
        ui.label('CREAR NUEVA RECETA').style(
            'font-size: 2rem; '
            'font-weight: bold; '
            'text-align: center; '
            'color: #e2e8f0; '
            'margin-bottom: 2rem; '
            'text-shadow: 0 2px 4px rgba(0,0,0,0.3);'
        )
        
        # Información básica
        with ui.card().style(
            'background: #1e293b; '
            'border: 2px solid #475569; '
            'border-radius: 12px; '
            'padding: 1.5rem; '
            'margin-bottom: 1.5rem;'
        ):
            ui.label('INFORMACIÓN BÁSICA').style(
                'font-size: 1.1rem; '
                'font-weight: bold; '
                'color: #93c5fd; '
                'margin-bottom: 1rem;'
            )
            
            nombre_input = ui.input('Nombre de la receta', placeholder='Ej: Pasta Carbonara').props(
                'outlined bg-color=blue-grey-9 label-color=blue-2'
            ).classes('w-full mb-3').style('color: #e2e8f0;')
            
            desc_input = ui.textarea('Descripción (opcional)', placeholder='Breve descripción de la receta...').props(
                'outlined bg-color=blue-grey-9 label-color=blue-2 rows=3'
            ).classes('w-full').style('color: #e2e8f0;')
        
        # Separador
        ui.separator().style('background: #475569; margin: 1.5rem 0; height: 2px;')
        
        # Sección de pasos
        with ui.row().classes('w-full items-center mb-4'):
            ui.label('PASOS DE LA RECETA').style(
                'font-size: 1.2rem; '
                'font-weight: bold; '
                'color: #93c5fd;'
            )
            ui.space()
            ui.button('Agregar Paso', icon='add', on_click=agregar_paso).props(
                'color=blue-6 size=md'
            ).style(
                'font-weight: 600; '
                'padding: 0.5rem 1.2rem; '
                'border-radius: 10px;'
            )
        
        # Lista de pasos con scroll
        with ui.scroll_area().style(
            'width: 100%; '
            'height: 400px; '
            'background: #0f172a; '
            'border: 2px solid #334155; '
            'border-radius: 12px; '
            'padding: 1rem;'
        ):
            pasos_list = ui.column().classes('w-full')
        
        # Separador
        ui.separator().style('background: #475569; margin: 1.5rem 0; height: 2px;')
        
        # Botones de acción
        with ui.row().classes('w-full justify-end gap-3'):
            ui.button('Cancelar', on_click=dialog.close).props(
                'outline color=red-6 size=lg'
            ).style(
                'font-weight: 600; '
                'padding: 0.7rem 2rem; '
                'border-radius: 10px;'
            )
            ui.button('Guardar Receta', icon='save', on_click=guardar).props(
                'color=green-6 size=lg'
            ).style(
                'font-weight: 600; '
                'padding: 0.7rem 2rem; '
                'border-radius: 10px;'
            )
        
        # Agregar el primer paso automáticamente
        agregar_paso()
    
    dialog.open()

def mostrar_menu_configuracion():
    """Muestra el menú de configuración - PROFESIONAL"""
    def confirmar_reset():
        recetas_ctrl.reiniciar_fabrica()
        ui.notify('Recetas de usuario eliminadas', type='positive')
        dialog.close()
    
    # DIÁLOGO PROFESIONAL
    with ui.dialog() as dialog, ui.card().style(
        'background: linear-gradient(145deg, #1e293b, #0f172a); '
        'border: 2px solid #334155; '
        'border-radius: 20px; '
        'padding: 2.5rem; '
        'min-width: 450px; '
        'max-width: 550px; '
        'box-shadow: 0 20px 40px rgba(0,0,0,0.6);'
    ):
        # Título
        ui.label('CONFIGURACIÓN').style(
            'font-size: 2rem; '
            'font-weight: bold; '
            'text-align: center; '
            'color: #e2e8f0; '
            'margin-bottom: 2rem; '
            'text-shadow: 0 2px 4px rgba(0,0,0,0.3);'
        )
        
        # Información del sistema
        with ui.card().style(
            'background: #1e293b; '
            'border: 2px solid #475569; '
            'border-radius: 12px; '
            'padding: 1.5rem; '
            'margin-bottom: 1.5rem;'
        ):
            ui.label('INFORMACIÓN DEL SISTEMA').style(
                'font-size: 1.1rem; '
                'font-weight: bold; '
                'color: #93c5fd; '
                'margin-bottom: 1rem;'
            )
            
            with ui.column().classes('gap-2'):
                ui.label('Versión: 2.0.0 - Final').style('color: #cbd5e1; font-size: 1rem;')
                ui.label('Modo: Control Manual').style('color: #cbd5e1; font-size: 1rem;')
                ui.label('Base de datos: SQLite').style('color: #cbd5e1; font-size: 1rem;')
                ui.label('Framework: NiceGUI + Python').style('color: #cbd5e1; font-size: 1rem;')
        
        # Separador
        ui.separator().style('background: #475569; margin: 1.5rem 0; height: 2px;')
        
        # Acciones peligrosas
        with ui.card().style(
            'background: #7f1d1d; '
            'border: 2px solid #991b1b; '
            'border-radius: 12px; '
            'padding: 1.5rem; '
            'margin-bottom: 1.5rem;'
        ):
            ui.label('ZONA PELIGROSA').style(
                'font-size: 1.1rem; '
                'font-weight: bold; '
                'color: #fca5a5; '
                'margin-bottom: 1rem;'
            )
            
            ui.label('Esta acción eliminará todas tus recetas personalizadas. Las recetas preinstaladas se mantendrán intactas.').style(
                'color: #fecaca; '
                'font-size: 1rem; '
                'margin-bottom: 1rem; '
                'line-height: 1.6;'
            )
            
            ui.button('Reiniciar de Fábrica', icon='restore', on_click=confirmar_reset).props(
                'color=red-7 size=md'
            ).classes('w-full').style(
                'font-weight: 600; '
                'padding: 0.8rem; '
                'border-radius: 10px;'
            )
        
        # Separador
        ui.separator().style('background: #475569; margin: 1.5rem 0; height: 2px;')
        
        # Botón cerrar
        with ui.row().classes('w-full justify-center'):
            ui.button('Cerrar', on_click=dialog.close).props(
                'color=blue-6 size=lg'
            ).style(
                'font-weight: 600; '
                'padding: 0.7rem 3rem; '
                'border-radius: 10px;'
            )
    
    dialog.open()

def crear_boton_funcion(icono: str, texto: str, color: str, callback):
    """Crea un botón de función estilo Thermomix"""
    with ui.column().classes('items-center gap-3').style('width: 140px'):
        ui.button(icon=icono, on_click=callback).props(f'round size=xl').style(
            f'width: 100px; height: 100px; background: {color}; box-shadow: 0 6px 0 {color}dd, 0 10px 20px rgba(0,0,0,0.3);'
        ).classes('thermomix-btn')
        ui.label(texto).classes('text-base font-bold text-center').style(
            'color: #e2e8f0; '
            'text-shadow: 0 2px 4px rgba(0,0,0,0.3); '
            'letter-spacing: 0.5px;'
        )

# ========== CONTINUACIÓN PARTE 3/3 - FINAL ==========

def crear_interfaz():
    """Crea la interfaz principal tipo Thermomix"""
    global estado_led, estado_texto, pantalla_paso, pantalla_info
    global barra_progreso, label_progreso, log_area
    global boton_accion_principal, label_accion, boton_anterior
    
    robot_ctrl.set_callback_log(agregar_log)
    robot_ctrl.set_callback_estado(actualizar_estado_ui)
    robot_ctrl.set_callback_progreso(actualizar_progreso)
    
    # ==========================================
    # HEAD COMPLETO CON ESTILOS
    # ==========================================
    ui.add_head_html('''
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Robot de Cocina Inteligente - Control paso a paso de recetas">
        <meta name="author" content="Sistema de Control de Robot">
        <title>Robot de Cocina | Control Inteligente</title>
        <link rel="shortcut icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%230f172a' width='100' height='100'/%3E%3Ccircle cx='50' cy='50' r='35' fill='%233b82f6' stroke='%2393c5fd' stroke-width='3'/%3E%3Cpath d='M35 45L50 35L65 45M50 35V65M40 55Q50 60 60 55' stroke='%23fff' stroke-width='4' fill='none' stroke-linecap='round'/%3E%3Ccircle cx='50' cy='70' r='3' fill='%2310b981'/%3E%3C/svg%3E">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            html {
                font-size: 16px;
            }
            
            body { 
                background: #0f172a;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .thermomix-body {
                background: linear-gradient(145deg, #1e293b, #0f172a);
                border: 3px solid #334155;
                border-radius: 30px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.5);
                width: 900px;
                max-width: 95vw;
                padding: 3rem;
                margin: 2rem auto;
            }
            
            .thermomix-btn:active {
                transform: translateY(4px);
                box-shadow: 0 2px 0 currentColor !important;
            }
            
            .pantalla-lcd {
                background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
                color: #93c5fd;
                font-family: 'Courier New', monospace;
                border: 2px solid #2563eb;
            }
            
            .nicegui-content {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                min-height: 100vh !important;
                width: 100% !important;
                padding: 1rem;
            }
            
            .log-terminal {
                background: #1e293b !important;
                color: #94a3b8 !important;
                border: 2px solid #334155 !important;
                font-family: 'Consolas', 'Monaco', monospace !important;
            }
            
            .log-terminal textarea {
                color: #94a3b8 !important;
                background: #1e293b !important;
            }
            
            .q-field__control {
                color: #94a3b8 !important;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.8; transform: scale(1.05); }
            }
            
            /* Mejorar scroll en diálogos */
            .q-dialog__inner {
                padding: 1rem;
            }
            
            /* Scrollbar personalizado */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #1e293b;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #475569;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #64748b;
            }
        </style>
    ''')
    
    # ==========================================
    # BODY - ESTRUCTURA PRINCIPAL
    # ==========================================
    with ui.column().classes('items-center justify-center').style('width: 100vw; min-height: 100vh;'):
        with ui.card().classes('thermomix-body'):
            
            # ========== PANTALLA LCD ==========
            with ui.card().classes('pantalla-lcd w-full mb-6').style('padding: 2rem; min-height: 220px'):
                with ui.row().classes('w-full items-center mb-4'):
                    estado_led = ui.element('div').style(
                        'width: 24px; height: 24px; border-radius: 50%; background: #dc2626; '
                        'box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);'
                    )
                    ui.space()
                    estado_texto = ui.label('APAGADO').classes('text-3xl font-bold').style('color: #93c5fd;')
                
                pantalla_paso = ui.label('No hay receta cargada').classes('text-2xl text-center font-bold mb-3').style('color: #bfdbfe;')
                
                # ⭐ TEXTO DE INFO MÁS GRANDE Y LEGIBLE ⭐
                pantalla_info = ui.label('Selecciona una receta para comenzar').classes('text-center').style(
                    'color: #cbd5e1; '
                    'white-space: pre-line; '
                    'font-size: 1.1rem; '
                    'line-height: 1.6; '
                    'font-weight: 500;'
                )
                
                ui.separator().style('background: #3b82f6; opacity: 0.3; margin: 1.5rem 0')
                
                with ui.row().classes('w-full items-center gap-4'):
                    with ui.column().classes('flex-1'):
                        # ⭐ LABEL PROGRESO MÁS LEGIBLE ⭐
                        ui.label('PROGRESO').style(
                            'font-size: 0.95rem; '
                            'font-weight: bold; '
                            'color: #cbd5e1; '
                            'letter-spacing: 1px;'
                        )
                        barra_progreso = ui.linear_progress(value=0).classes('w-full').style('height: 12px;')
                    label_progreso = ui.label('0/0').classes('text-xl font-bold').style('color: #93c5fd;')
            
            # ========== BOTONES DE CONTROL ==========
            with ui.row().classes('w-full justify-center gap-8 mb-8 mt-2'):
                crear_boton_funcion('power_settings_new', 'ENCENDER', '#10b981', on_encender)
                crear_boton_funcion('power_off', 'APAGAR', '#ef4444', on_apagar)
            
            ui.separator().style('margin: 2rem 0; background: #475569; height: 3px;')
            
            # ========== BOTÓN ÚNICO CONTEXTUAL ==========
            with ui.row().classes('w-full justify-center gap-6 mb-6 mt-6'):
                # Botón Anterior
                with ui.column().classes('items-center gap-3').style('width: 140px'):
                    boton_anterior = ui.button(icon='arrow_back', on_click=anterior_paso).props('round size=xl').style(
                        'width: 100px; height: 100px; background: #6b7280; box-shadow: 0 6px 0 #6b7280dd, 0 10px 20px rgba(0,0,0,0.3);'
                    ).classes('thermomix-btn')
                    boton_anterior.enabled = False
                    ui.label('ANTERIOR').classes('text-base font-bold text-center').style(
                        'color: #e2e8f0; '
                        'text-shadow: 0 2px 4px rgba(0,0,0,0.3); '
                        'letter-spacing: 0.5px;'
                    )
                
                # BOTÓN PRINCIPAL CONTEXTUAL
                with ui.column().classes('items-center gap-3').style('width: 160px'):
                    boton_accion_principal = ui.button(icon='power_off', on_click=accion_principal_click).props('round size=xl').style(
                        'width: 140px; height: 140px; background: #6b7280; box-shadow: 0 8px 0 #6b7280dd, 0 12px 24px rgba(0,0,0,0.4); opacity: 0.5;'
                    ).classes('thermomix-btn')
                    boton_accion_principal.enabled = False
                    label_accion = ui.label('SIN RECETA').classes('text-lg font-bold text-center').style(
                        'color: #e2e8f0; '
                        'text-shadow: 0 2px 4px rgba(0,0,0,0.3); '
                        'letter-spacing: 0.5px;'
                    )
            
            ui.separator().style('margin: 2rem 0; background: #475569; height: 3px;')
            
            # ========== BOTONES DE FUNCIONES ==========
            with ui.row().classes('w-full justify-center gap-8 mb-8 mt-6'):
                crear_boton_funcion('restaurant_menu', 'RECETAS', '#3b82f6', seleccionar_receta)
                crear_boton_funcion('add_circle', 'CREAR', '#06b6d4', mostrar_menu_crear_receta)
                crear_boton_funcion('settings', 'CONFIG', '#6b7280', mostrar_menu_configuracion)
            
            ui.separator().style('margin: 2rem 0; background: #475569;')
            
            # ========== LOG DE ACTIVIDAD ==========
            # ⭐ LABEL MÁS GRANDE Y LEGIBLE ⭐
            ui.label('REGISTRO DE ACTIVIDAD').style(
                'font-size: 1.1rem; '
                'font-weight: bold; '
                'color: #cbd5e1; '
                'letter-spacing: 1px; '
                'margin-bottom: 0.8rem;'
            )
            log_area = ui.textarea(value='Sistema iniciado...').classes('w-full log-terminal').props('readonly outlined dense').style(
                'height: 150px; font-family: Consolas, Monaco, monospace; font-size: 13px; line-height: 1.5;'
            )
    
    # ========== LOGS INICIALES ==========
    agregar_log('=' * 50)
    agregar_log('ROBOT DE COCINA v2.0 - SISTEMA INICIADO')
    agregar_log('=' * 50)
    agregar_log('INSTRUCCIONES:')
    agregar_log('1. Pulsa ENCENDER para activar el robot')
    agregar_log('2. Selecciona una receta del menu RECETAS')
    agregar_log('3. Pulsa COCINAR para ejecutar el paso')
    agregar_log('4. El boton cambiara segun el estado')
    agregar_log('=' * 50)
    agregar_log('Sistema listo para operar')
    agregar_log('')

# ========== FIN PARTE 3/3 - CÓDIGO COMPLETO ==========