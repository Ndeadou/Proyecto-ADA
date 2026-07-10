"""
Módulo: gestor_tareas.py
-------------------------
Clase principal que integra el MaxHeap (cola de prioridad) y el
ArbolAVL (índice por id) para formar el sistema completo de
gestión de tareas.

Cada operación que modifica el estado (agregar/eliminar) debe
actualizar AMBAS estructuras para mantenerlas sincronizadas.
"""

from heap import MaxHeap, Tarea
from avl import ArbolAVL


class GestorTareas:
    def __init__(self):
        self.heap = MaxHeap()
        self.avl = ArbolAVL()
        self._siguiente_id = 1  # generador simple de ids únicos

    def agregar_tarea(self, descripcion, prioridad, fecha_vencimiento, id_tarea=None):
        """
        Agrega una tarea al sistema: se inserta en AMBAS estructuras.
        Si no se especifica id_tarea, se genera uno automáticamente.
        """
        if id_tarea is None:
            id_tarea = self._siguiente_id
            self._siguiente_id += 1
        else:
            self._siguiente_id = max(self._siguiente_id, id_tarea + 1)

        tarea = Tarea(id_tarea, descripcion, prioridad, fecha_vencimiento)

        self.heap.insertar(tarea)
        self.avl.insertar(tarea)

        return tarea

    def eliminar_tarea(self, id_tarea):
        """
        Elimina una tarea del sistema (por ejemplo, al marcarla como
        completada). Se elimina de AMBAS estructuras.
        """
        tarea_eliminada = self.heap.eliminar_por_id(id_tarea)
        self.avl.eliminar(id_tarea)
        return tarea_eliminada

    def buscar_tarea(self, id_tarea):
        """
        Busca una tarea por su id usando el árbol AVL. O(log n)
        Esta es la ventaja principal de mantener el índice AVL:
        búsquedas rápidas sin tener que recorrer todo el heap.
        """
        return self.avl.buscar(id_tarea)

    def obtener_tarea_mas_prioritaria(self):
        """Retorna (sin eliminar) la tarea de mayor prioridad. O(1)"""
        return self.heap.ver_maximo()

    def completar_tarea_mas_prioritaria(self):
        """
        Extrae y elimina la tarea de mayor prioridad del sistema
        (equivalente a "completarla"). Se elimina de AMBAS estructuras.
        """
        tarea = self.heap.extraer_maximo()
        if tarea:
            self.avl.eliminar(tarea.id)
        return tarea

    def listar_todas_por_id(self):
        """Retorna todas las tareas ordenadas por id (recorrido in-order del AVL)."""
        return self.avl.in_order()

    def cantidad_tareas(self):
        return self.heap.tamano()


# ---------- Pruebas del sistema integrado (simula el caso de uso del enunciado) ----------
if __name__ == "__main__":
    gestor = GestorTareas()

    gestor.agregar_tarea("Estudiar para el examen", "Alta", "2026-07-10", id_tarea=101)
    gestor.agregar_tarea("Comprar útiles escolares", "Media", "2026-07-12", id_tarea=102)
    gestor.agregar_tarea("Revisar correos electrónicos", "Baja", "2026-07-09", id_tarea=103)

    print("--- Prueba de búsqueda (árbol AVL) ---")
    print("Buscar id=102:", gestor.buscar_tarea(102))

    print("\n--- Prueba de prioridad (heap) ---")
    print("Tarea más prioritaria:", gestor.obtener_tarea_mas_prioritaria())

    print("\n--- Prueba de completar tarea ---")
    completada = gestor.completar_tarea_mas_prioritaria()
    print("Se completó:", completada)
    print("Ahora, ¿existe id=101 en el AVL?:", gestor.buscar_tarea(101))
    print("Nueva tarea más prioritaria:", gestor.obtener_tarea_mas_prioritaria())

    print("\n--- Listado final ordenado por id ---")
    for t in gestor.listar_todas_por_id():
        print(" ", t)
