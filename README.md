#Integrantes: Miguel Descance, Erick Obando

# Gestor de Tareas con Cola de Prioridad (Heap) y Árbol AVL

Sistema de gestión de tareas para una aplicación de productividad. Combina un
**montículo binario (Max-Heap)** para priorizar tareas y un **árbol AVL**
para indexarlas por su identificador único, garantizando búsquedas eficientes
en O(log n).

## Integrantes del grupo

- Nombre 1
- Nombre 2
- Nombre 3

## Estructuras de datos utilizadas

| Estructura | Archivo | Propósito |
|---|---|---|
| Max-Heap | `heap.py` | Gestiona las tareas según su prioridad (Alta > Media > Baja). Permite obtener la tarea más urgente en O(1) y extraerla en O(log n). |
| Árbol AVL | `avl.py` | Indexa las tareas por su `id` único. Se autobalancea tras cada inserción/eliminación mediante rotaciones (LL, RR, LR, RL), garantizando búsquedas en O(log n). |
| Integración | `gestor_tareas.py` | Clase `GestorTareas` que sincroniza ambas estructuras: cada operación de agregar/eliminar actualiza el heap y el AVL a la vez. |
| Interfaz gráfica | `gui.py` | GUI construida con `tkinter` para interactuar con el sistema visualmente. |
| Pruebas | `test_casos.py` | Casos de prueba formales: inserción, eliminación, indexación y equilibrio. |

## Requisitos

- Python 3.8 o superior
- No requiere librerías externas: todo el proyecto usa únicamente la librería estándar de Python (`tkinter`, `unittest`, `time`, `random`).

> **Nota para Windows:** `tkinter` viene incluido por defecto en el instalador oficial de Python (python.org). No es necesario instalar nada adicional.

## Cómo ejecutar el programa

1. Clonar el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd <nombre-de-la-carpeta>
   ```

2. Ejecutar la interfaz gráfica:
   ```bash
   python gui.py
   ```
   (En algunos sistemas puede requerirse `python3` en lugar de `python`.)

3. Se abrirá una ventana donde se puede:
   - Agregar una nueva tarea (descripción, prioridad, fecha de vencimiento).
   - Ver la tarea más prioritaria en cola.
   - Completar (eliminar) la tarea más prioritaria.
   - Buscar o eliminar cualquier tarea por su ID.
   - Ver todas las tareas ordenadas por ID en una tabla.

## Cómo ejecutar las pruebas

Desde la raíz del proyecto:

```bash
python -m unittest test_casos.py -v
```

Esto ejecuta 15 pruebas divididas en 4 categorías:

- **Prueba de inserción**: verifica que las tareas se insertan correctamente en ambas estructuras y que el orden de extracción respeta la prioridad.
- **Prueba de eliminación**: verifica que al eliminar una tarea (la más prioritaria o cualquier otra), la estructura del heap se mantiene válida.
- **Prueba de indexación**: verifica búsquedas correctas por ID, con 1000 tareas de prueba, y confirma tiempos de respuesta eficientes.
- **Prueba de equilibrio**: verifica que el árbol AVL se rebalancea correctamente ante los 4 casos de rotación (LL, RR, LR, RL) y ante secuencias de inserción desbalanceadas.

También se puede ejecutar cada módulo individualmente para ver una demostración rápida por consola:

```bash
python heap.py
python avl.py
python gestor_tareas.py
```

## Estructura del repositorio

```
.
├── heap.py             # Max-Heap (cola de prioridad)
├── avl.py               # Árbol AVL (indexación por ID)
├── gestor_tareas.py      # Integración de ambas estructuras
├── gui.py                # Interfaz gráfica (tkinter)
├── test_casos.py         # Casos de prueba formales (unittest)
└── README.md
```

## Complejidad de las operaciones

| Operación | Complejidad | Estructura |
|---|---|---|
| Insertar tarea | O(log n) | Heap + AVL |
| Buscar tarea por ID | O(log n) | AVL |
| Obtener tarea más prioritaria | O(1) | Heap |
| Extraer/completar tarea más prioritaria | O(log n) | Heap |
| Eliminar tarea arbitraria por ID | O(n) | Heap (búsqueda lineal) + O(log n) (AVL) |
