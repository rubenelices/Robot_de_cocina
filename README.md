# 🤖 Robot de Cocina - Sistema de Control Inteligente

## 📋 Descripción

Sistema completo de control para robot de cocina desarrollado en Python con arquitectura POO (Programación Orientada a Objetos). El sistema permite gestionar recetas preinstaladas y personalizadas, ejecutar procesos de cocina simulados mediante hilos, y controlar el robot a través de una interfaz web moderna.

## ✨ Características Principales

- **Interfaz Web Moderna**: Desarrollada con NiceGUI, intuitiva y responsive
- **Arquitectura POO**: Implementación completa de abstracción, herencia, polimorfismo y encapsulación
- **Ejecución Concurrente**: Uso de threading para operaciones no bloqueantes
- **Base de Datos SQLite**: Persistencia de recetas base y personalizadas
- **9 Procesos de Cocina**: Picar, Rallar, Triturar, Trocear, Amasar, Hervir, Sofreír, Vapor y PrepararPuré
- **Gestión de Recetas**: CRUD completo para recetas personalizadas
- **Reinicio de Fábrica**: Elimina datos de usuario manteniendo recetas preinstaladas

## 🏗️ Estructura del Proyecto

```
robot/
│
├── app.py                          # Punto de entrada principal
├── main.py                         # Configuración y constantes
├── README.md                       # Este archivo
│
├── database/                       # Capa de datos
│   ├── db.py                      # Gestor de base de datos
│   └── init_db.py                 # Inicialización y datos preinstalados
│
├── models/                         # Modelos de dominio (POO)
│   ├── proceso.py                 # Clase abstracta ProcesoCocina
│   ├── procesos_basicos.py        # Implementaciones concretas (9 procesos)
│   ├── receta.py                  # Modelo Receta
│   └── robot.py                   # Modelo RobotCocina
│
├── controllers/                    # Controladores (lógica de negocio)
│   ├── robot_controller.py        # Controlador del robot
│   └── recetas_controller.py      # Controlador de recetas
│
├── ui/                            # Interfaz de usuario
│   ├── interfaz.py                # Interfaz NiceGUI
│   └── styles.css                 # Estilos personalizados
│
└── utils/                         # Utilidades
    ├── exceptions.py              # Excepciones personalizadas
    └── threading_manager.py       # Gestor de hilos
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar o descomprimir el proyecto
cd robot

# Instalar dependencias
pip install nicegui
```

**Nota**: NiceGUI es la única dependencia externa. SQLite viene incluido con Python.

## ▶️ Ejecución

### Método Simple

```bash
python app.py
```

### El sistema automáticamente:
1. Inicializa la base de datos SQLite
2. Carga 10 recetas preinstaladas
3. Inicia el servidor web en `http://localhost:8080`
4. Abre automáticamente el navegador

### Acceso Manual

Si el navegador no se abre automáticamente, accede a:
```
http://localhost:8080
```

## 🎯 Uso del Sistema

### 1. Encender el Robot

- Haz clic en el botón **"⚡ Encender"**
- El estado cambiará a **ENCENDIDO** (verde)
- Los controles se habilitarán

### 2. Ejecutar una Receta Preinstalada

1. Selecciona una receta del menú **"Recetas Preinstaladas"**
2. Haz clic en **"▶️ Ejecutar Receta"**
3. Observa el progreso en tiempo real:
   - Barra de progreso
   - Logs detallados de cada paso
   - Estado del robot

### 3. Crear Recetas Personalizadas

1. Haz clic en **"➕ Nueva Receta"**
2. Ingresa nombre y descripción
3. Haz clic en **"🔧 Agregar Proceso"**
4. Selecciona la receta y el tipo de proceso
5. Define parámetros y duración
6. La nueva receta aparecerá en **"Recetas Personalizadas"**

### 4. Detener Ejecución

- Durante la ejecución, haz clic en **"🛑 Parar"**
- El robot se detendrá de forma segura
- El estado cambiará a **DETENIDO**

### 5. Reinicio de Fábrica

- Haz clic en **"🔄 Reiniciar Fábrica"**
- Confirma la acción
- Se eliminarán **todas las recetas personalizadas**
- Las recetas preinstaladas permanecerán intactas

## 🧩 Diseño POO

### Abstracción

**Clase Abstracta: `ProcesoCocina`**

```python
class ProcesoCocina(ABC):
    @abstractmethod
    def ejecutar(self, callback):
        pass
    
    @abstractmethod
    def get_duracion(self) -> int:
        pass
    
    @abstractmethod
    def get_descripcion(self) -> str:
        pass
```

Define la interfaz común para todos los procesos de cocina, obligando a las subclases a implementar los métodos esenciales.

### Herencia

**9 Subclases Concretas:**

1. **Picar**: Corte fino de ingredientes
2. **Rallar**: Rallado de alimentos
3. **Triturar**: Triturado a alta velocidad
4. **Trocear**: Corte en cubos
5. **Amasar**: Amasado de masas
6. **Hervir**: Cocción por ebullición
7. **Sofreir**: Sofrito con aceite
8. **Vapor**: Cocción al vapor
9. **PrepararPure**: Preparación de purés

Cada una hereda de `ProcesoCocina` e implementa su comportamiento específico.

### Polimorfismo

```python
# Todas las subclases pueden usarse de forma intercambiable
procesos: List[ProcesoCocina] = [
    Picar("cebolla"),
    Triturar("velocidad=alta"),
    Hervir("temperatura=100C")
]

for proceso in procesos:
    proceso.ejecutar()  # Cada uno ejecuta su implementación
```

### Encapsulación

**Clase `RobotCocina`:**

```python
class RobotCocina:
    def __init__(self):
        self.__estado = ESTADO_APAGADO        # Atributo privado
        self.__proceso_actual = None          # Atributo privado
        
    @property
    def estado(self) -> str:                  # Getter público
        return self.__estado
    
    def __cambiar_estado(self, nuevo):        # Método privado
        self.__estado = nuevo
```

Los atributos internos son privados (prefijo `__`) y solo se accede mediante propiedades y métodos públicos.

## 🔄 Concurrencia con Threading

### ¿Por Qué Threading?

1. **No Bloquear la UI**: La interfaz permanece responsive durante la ejecución
2. **Operaciones Largas**: Las recetas pueden durar varios minutos
3. **Actualizaciones en Tiempo Real**: Los logs se actualizan mientras se ejecuta

### Implementación

**ThreadingManager:**

```python
class ThreadingManager:
    def ejecutar_en_hilo(self, funcion, *args, **kwargs):
        hilo = threading.Thread(
            target=funcion,
            args=args,
            kwargs=kwargs,
            daemon=True
        )
        hilo.start()
        return hilo
```

**Uso en el Controlador:**

```python
def ejecutar_receta_async(self, receta, callback_completado):
    def wrapper():
        exito = self._robot.ejecutar_receta(receta)
        if callback_completado:
            callback_completado(exito)
    
    self._thread_manager.ejecutar_en_hilo(wrapper)
```

### Ventajas

- ✅ La UI nunca se congela
- ✅ El usuario puede detener la ejecución en cualquier momento
- ✅ Múltiples callbacks actualizan la interfaz en tiempo real
- ✅ Manejo seguro de excepciones en hilos separados

## 🗄️ Base de Datos

### Esquema

#### Tablas Base (Preinstaladas)

```sql
CREATE TABLE recetas_base (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

CREATE TABLE procesos_base (
    id INTEGER PRIMARY KEY,
    receta_id INTEGER NOT NULL,
    tipo_proceso TEXT NOT NULL,
    parametros TEXT,
    orden INTEGER NOT NULL,
    duracion INTEGER NOT NULL,
    FOREIGN KEY (receta_id) REFERENCES recetas_base(id)
);
```

#### Tablas Usuario (Personalizadas)

```sql
CREATE TABLE recetas_usuario (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

CREATE TABLE procesos_usuario (
    id INTEGER PRIMARY KEY,
    receta_id INTEGER NOT NULL,
    tipo_proceso TEXT NOT NULL,
    parametros TEXT,
    orden INTEGER NOT NULL,
    duracion INTEGER NOT NULL,
    FOREIGN KEY (receta_id) REFERENCES recetas_usuario(id)
);
```

### Recetas Preinstaladas

El sistema incluye 10 recetas reales:

1. **Gazpacho Andaluz** - Sopa fría de tomate
2. **Puré de Patatas** - Cremoso puré tradicional
3. **Salsa Boloñesa** - Salsa italiana de carne
4. **Hummus Casero** - Pasta de garbanzos
5. **Masa de Pizza** - Masa italiana tradicional
6. **Ensalada de Zanahoria** - Zanahoria rallada fresca
7. **Verduras al Vapor** - Cocción saludable
8. **Sopa de Verduras** - Sopa nutritiva
9. **Pesto Genovés** - Salsa de albahaca
10. **Smoothie Tropical** - Batido de frutas

## ⚙️ Configuración

### Modificar Puerto del Servidor

En `app.py`:

```python
ui.run(
    title="Robot de Cocina",
    port=8080,  # Cambiar aquí
    reload=False,
    show=True
)
```

### Agregar Nuevos Procesos

1. Crear clase en `models/procesos_basicos.py`:

```python
class MiNuevoProceso(ProcesoCocina):
    def ejecutar(self, callback):
        # Implementación
        pass
    
    def get_duracion(self):
        return 10
    
    def get_descripcion(self):
        return "Mi proceso personalizado"
```

2. Registrar en el diccionario:

```python
PROCESOS_DISPONIBLES = {
    'MiNuevoProceso': MiNuevoProceso,
    # ... otros procesos
}
```

## 🐛 Solución de Problemas

### Error: "Module nicegui not found"

```bash
pip install nicegui
```

### Error: "Address already in use"

Otro proceso está usando el puerto 8080. Cambiar el puerto en `app.py` o detener el proceso:

```bash
# Linux/Mac
lsof -ti:8080 | xargs kill -9

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### La interfaz no se actualiza

- Verifica que el robot esté encendido
- Revisa la consola para errores de Python
- Recarga la página (F5)

## 📚 Dependencias

- **Python**: 3.8+
- **NiceGUI**: Framework web moderno para Python
- **SQLite**: Base de datos incluida en Python

## 👨‍💻 Desarrollo

### Ejecutar con Recarga Automática

Para desarrollo, activar el modo reload en `app.py`:

```python
ui.run(reload=True, show=False)
```

### Testing Manual

1. Encender robot
2. Ejecutar receta corta (ej: Zanahoria Rallada)
3. Probar detención a mitad de ejecución
4. Crear receta personalizada
5. Agregar procesos
6. Ejecutar receta personalizada
7. Reiniciar de fábrica
8. Verificar que solo las recetas usuario desaparecen

## 📄 Licencia

Proyecto académico - Uso educativo

## 🤝 Contribuciones

Este es un proyecto académico cerrado. Para proyectos similares, considera:
- Agregar autenticación de usuarios
- Implementar API REST
- Añadir simulación 3D del robot
- Integrar con hardware real

## 📞 Soporte

Para problemas técnicos:
1. Verifica la instalación de dependencias
2. Revisa los logs en la consola
3. Consulta la sección de solución de problemas

---

**Desarrollado con ❤️ usando Python y POO**