# Thermomix - Robot de Cocina Inteligente

Aplicación de simulación de un robot de cocina inteligente tipo Thermomix, desarrollada en Python con interfaz web moderna utilizando NiceGUI. El proyecto implementa un sistema completo de gestión de recetas y control de procesos de cocina, con una interfaz premium inspirada en dispositivos Thermomix reales.

## Descripción del Proyecto

Este proyecto es una simulación completa de un robot de cocina multifunción que permite:

- Ejecutar recetas predefinidas paso a paso
- Crear recetas personalizadas mediante un asistente guiado
- Control manual de 10 modos de cocción diferentes
- Gestión de ingredientes y favoritos
- Interfaz moderna y responsive con modo oscuro

## Características Principales

### Funcionalidades del Robot

- **Máquina de Estados**: Implementación robusta de una máquina de estados para el control del robot (apagado, encendido, ejecutando, detenido)
- **10 Modos de Cocción**:
  - Picar
  - Rallar
  - Triturar
  - Trocear
  - Amasar
  - Hervir
  - Sofreír
  - Vapor
  - Preparar Puré
  - Pesar

- **Ejecución de Procesos**: Sistema de simulación de procesos con callbacks y control de progreso en tiempo real
- **Sistema de Detención**: Capacidad de detener procesos en ejecución de forma segura

### Sistema de Recetas

- **Recetas Preinstaladas**: 10 recetas predefinidas que incluyen:
  - Gazpacho Andaluz
  - Puré de Patatas
  - Salsa Boloñesa
  - Hummus Casero
  - Masa de Pizza
  - Ensalada de Zanahoria
  - Verduras al Vapor
  - Sopa de Verduras
  - Pesto Genovés
  - Smoothie Tropical

- **Recetas de Usuario**: Crear, guardar y gestionar recetas personalizadas
- **Sistema de Favoritos**: Marcar recetas favoritas para acceso rápido
- **Gestión de Ingredientes**: Añadir ingredientes con cantidades y unidades específicas

### Interfaz de Usuario

#### Diseño

- **Paleta de Colores Thermomix**: Diseño con colores cyan, magenta, verde y naranja
- **Pantalla LCD Simulada**: Interfaz tipo LCD con efectos de brillo y bordes iluminados
- **Responsive**: Adaptado para dispositivos móviles, tablets y desktop

#### Componentes Principales

1. **Panel de Control**
   - Botón de encendido/apagado con efectos visuales
   - LED de estado con colores dinámicos
   - Indicadores de estado en tiempo real

2. **Selector de Modos**
   - 10 botones para modos de cocción manual
   - Indicadores visuales del modo activo
   - Sistema de recomendación de modo según la receta

3. **Navegador de Recetas**
   - Grid responsivo de tarjetas de recetas
   - Filtros: Todas, Base, Usuario, Favoritas
   - Búsqueda por texto
   - Vista previa con información detallada

4. **Panel de Ejecución**
   - Progreso paso a paso de la receta
   - Barra de progreso visual
   - Log de ejecución en tiempo real
   - Controles de navegación (anterior/siguiente)
   - Pantalla de celebración al completar receta

5. **Wizard de Creación**
   - Asistente en 3 pasos para crear recetas
   - Paso 1: Información básica (nombre, descripción)
   - Paso 2: Gestión de ingredientes
   - Paso 3: Configuración de procesos de cocción

## Arquitectura del Proyecto

### Estructura de Directorios

```
robotcopia/
├── app.py                      # Punto de entrada principal
├── requirements.txt            # Dependencias del proyecto
├── robot_cocina.db            # Base de datos SQLite
│
├── models/                    # Capa de Modelos
│   ├── proceso.py            # Clase abstracta ProcesoCocina
│   ├── procesos_basicos.py   # Implementaciones concretas (Picar, Triturar, etc.)
│   ├── receta.py             # Modelo de Receta
│   └── robot.py              # Modelo del RobotCocina
│
├── controllers/              # Capa de Controladores
│   ├── robot_controller.py  # Controlador del robot
│   └── recetas_controller.py # Controlador de recetas 
│
├── database/                 # Capa de Datos
│   ├── db.py                # DatabaseManager (SQLite)
│   └── init_db.py           # Inicialización y migraciones
│
├── ui/                       # Capa de Interfaz
│   ├── interfaz.py          # Interfaz principal
│   ├── components/          # Componentes UI reutilizables
│   │   ├── common.py        # Componentes comunes
│   │   ├── mode_selector.py # Selector de modos
│   │   ├── recipe_browser.py # Navegador de recetas
│   │   └── execution_panel.py # Panel de ejecución
│   ├── state/
│   │   └── app_state.py     # Estado centralizado de la aplicación
│   └── styles/
│       ├── colors.py        # Paleta de colores
│       └── tailwind_config.py # Configuración Tailwind
│
└── utils/                    # Utilidades
    ├── exceptions.py        # Excepciones personalizadas
    └── threading_manager.py # Gestión de hilos
```

### Patrones de Diseño Implementados

#### 1. Patrón MVC (Model-View-Controller)

- **Models**: Clases `Robot`, `Receta`, `ProcesoCocina` y sus derivadas
- **Views**: Componentes de UI en `ui/components/`
- **Controllers**: `RobotController`, `RecetasController`

#### 2. Patrón Factory

Implementado en `procesos_basicos.py`:

```python
def crear_proceso(tipo: str, parametros: str, duracion: int) -> ProcesoCocina:
    """Factory function para crear procesos dinámicamente"""
    if tipo not in PROCESOS_DISPONIBLES:
        raise ValueError(f"Tipo de proceso '{tipo}' no reconocido")

    clase_proceso = PROCESOS_DISPONIBLES[tipo]
    return clase_proceso(parametros, duracion)
```

#### 3. Patrón State (Máquina de Estados)

Implementado en `RobotCocina` con transiciones de estado:
- `ESTADO_APAGADO` → `ESTADO_ENCENDIDO` → `ESTADO_EJECUTANDO` → `ESTADO_DETENIDO`

#### 4. Patrón Observer (Callbacks)

Sistema de callbacks para notificaciones de eventos:
- `callback_log`: Mensajes de log
- `callback_estado`: Cambios de estado del robot
- `callback_progreso`: Progreso de ejecución de receta

#### 5. Singleton

Estado centralizado de la aplicación en `app_state.py`:

```python
app_state = AppState()
```

#### 6. Template Method

Implementado en la clase abstracta `ProcesoCocina`:

```python
class ProcesoCocina(ABC):
    @abstractmethod
    def ejecutar(self, callback: Optional[Callable[[str], None]] = None) -> bool:
        """Método abstracto que las subclases deben implementar"""
        pass
```

### Principios SOLID Aplicados

#### Single Responsibility Principle (SRP)
- Cada clase tiene una única responsabilidad claramente definida
- `RobotCocina`: Control del robot
- `Receta`: Gestión de recetas
- `DatabaseManager`: Acceso a datos

#### Open/Closed Principle (OCP)
- Extensible mediante nuevos procesos sin modificar código existente
- Factory pattern permite agregar nuevos tipos de procesos

#### Liskov Substitution Principle (LSP)
- Todas las clases de proceso heredan de `ProcesoCocina` y son intercambiables

#### Interface Segregation Principle (ISP)
- Interfaces específicas para cada tipo de callback
- Métodos segregados por responsabilidad

#### Dependency Inversion Principle (DIP)
- Los controllers dependen de abstracciones (interfaces) no de implementaciones concretas
- Inyección de dependencias mediante callbacks

### Programación Orientada a Objetos

#### Encapsulación

Uso extensivo de atributos privados con propiedades:

```python
class RobotCocina:
    def __init__(self):
        self.__estado = ESTADO_APAGADO
        self.__proceso_actual = None

    @property
    def estado(self) -> str:
        return self.__estado
```

#### Herencia

Jerarquía de clases de procesos:

```
ProcesoCocina (Abstract)
    ├── Picar
    ├── Rallar
    ├── Triturar
    ├── Trocear
    ├── Amasar
    ├── Hervir
    ├── Sofreir
    ├── Vapor
    ├── PrepararPure
    └── Pesar
```

#### Polimorfismo

Cada proceso implementa su propio método `ejecutar()`:

```python
class Picar(ProcesoCocina):
    def ejecutar(self, callback):
        # Implementación específica de picar

class Triturar(ProcesoCocina):
    def ejecutar(self, callback):
        # Implementación específica de triturar
```

#### Abstracción

Clase base abstracta que define la interfaz común:

```python
class ProcesoCocina(ABC):
    @abstractmethod
    def ejecutar(self, callback) -> bool:
        pass

    @abstractmethod
    def get_duracion(self) -> int:
        pass
```

## Base de Datos

### Esquema (Versión 2.0)

#### Tablas Principales

**recetas_base**
- `id`: INTEGER PRIMARY KEY
- `nombre`: TEXT UNIQUE
- `descripcion`: TEXT

**procesos_base**
- `id`: INTEGER PRIMARY KEY
- `receta_id`: INTEGER (FK)
- `tipo_proceso`: TEXT
- `parametros`: TEXT
- `orden`: INTEGER
- `duracion`: INTEGER

**recetas_usuario**
- `id`: INTEGER PRIMARY KEY
- `nombre`: TEXT
- `descripcion`: TEXT
- `favorito`: INTEGER (0/1)
- `fecha_creacion`: DATETIME

**procesos_usuario**
- `id`: INTEGER PRIMARY KEY
- `receta_id`: INTEGER (FK CASCADE)
- `tipo_proceso`: TEXT
- `parametros`: TEXT
- `orden`: INTEGER
- `duracion`: INTEGER

**ingredientes** (Nuevo en v2.0)
- `id`: INTEGER PRIMARY KEY
- `receta_id`: INTEGER (FK CASCADE)
- `nombre`: TEXT
- `cantidad`: REAL
- `unidad`: TEXT
- `orden`: INTEGER
- `es_base`: BOOLEAN

**preferencias_usuario** (Nuevo en v2.0)
- `id`: INTEGER PRIMARY KEY
- `clave`: TEXT UNIQUE
- `valor`: TEXT

### Sistema de Migraciones

El proyecto incluye un sistema de migraciones automáticas que actualiza la base de datos de forma segura:

- Detección automática de versión actual
- Migración incremental a v2.0
- Preservación de datos existentes

## Instalación y Ejecución

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. Clonar el repositorio:
```bash
cd robotcopia
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Ejecución

```bash
python app.py
```

La aplicación se abrirá automáticamente en el navegador en `http://localhost:8080`

## Uso de la Aplicación

### Inicio Rápido

1. **Encender el Robot**: Presionar el botón de encendido (verde)
2. **Seleccionar una Receta**: Navegar al navegador de recetas y seleccionar una
3. **Ejecutar Paso a Paso**:
   - Seleccionar el modo de cocción recomendado
   - Presionar "Ejecutar Paso"
   - Observar el progreso en tiempo real
4. **Crear Receta Personalizada**: Usar el wizard de 3 pasos para crear tu propia receta

### Modo Manual

1. Encender el robot
2. Seleccionar un modo de cocción (Picar, Triturar, etc.)
3. Ejecutar el modo sin necesidad de una receta

### Gestión de Favoritos

- Click en el icono de estrella en cualquier receta de usuario para marcarla como favorita
- Filtrar por favoritas usando el selector de filtros

## Características Técnicas

### Concurrencia y Threading

- Sistema de ejecución asíncrona mediante asyncio
- Simulación de procesos con sleep no bloqueante
- Control de detención mediante flags

### Manejo de Excepciones

Excepciones personalizadas:
- `RobotApagadoException`: Intento de ejecutar con robot apagado
- `ProcesoInvalidoException`: Proceso no válido
- `RecetaNoEncontradaException`: Receta inexistente

### Logs y Debugging

- Sistema de logging en tiempo real
- Callbacks para tracking de eventos
- Estado centralizado para debugging

## Mejoras Futuras

### Funcionalidades Planificadas

- Exportación/importación de recetas en JSON
- Sistema de tags y categorías
- Temporizador con notificaciones
- Historial de recetas ejecutadas
- Integración con APIs de recetas externas
- Modo de voz para control por comandos
- Soporte multiidioma
- Gráficos de nutrición
- Compartir recetas con otros usuarios

### Optimizaciones Técnicas

- Cache de recetas en memoria
- Optimización de queries SQL
- Lazy loading de componentes UI
- WebSockets para comunicación en tiempo real
- Tests unitarios y de integración
- CI/CD pipeline
- Dockerización

## Tecnologías Utilizadas

- **Python 3.13**: Lenguaje principal
- **NiceGUI 1.4+**: Framework de interfaz web basado en Vue.js
- **SQLite**: Base de datos embebida
- **Asyncio**: Programación asíncrona
- **Tailwind CSS**: Framework CSS (integrado en NiceGUI)


Proyecto desarrollado como trabajo final para la asignatura de Desarrollo Orientado a Objetos, 3º de Ingeniería Matemática.

