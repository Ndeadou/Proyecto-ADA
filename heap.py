"""
Módulo: heap.py
----------------
Implementa un Montículo Binario (Max-Heap) para gestionar tareas
según su prioridad.

Estructura:
    El heap se representa internamente como una lista (arreglo).
    Para un nodo en la posición i:
        - hijo_izquierdo -> 2*i + 1
        - hijo_derecho   -> 2*i + 2
        - padre          -> (i - 1) // 2

Propiedad de Max-Heap:
    El valor (prioridad) de cada nodo padre es SIEMPRE mayor o igual
    que el valor de sus hijos. Esto garantiza que la raíz (índice 0)
    sea siempre el elemento de mayor prioridad.
"""


class Tarea:
    """Representa una tarea del sistema de productividad."""

    # Mapeo de prioridad textual a valor numérico (para el heap)
    PRIORIDADES = {"baja": 1, "media": 2, "alta": 3}

    def __init__(self, id_tarea, descripcion, prioridad, fecha_vencimiento):
        self.id = id_tarea
        self.descripcion = descripcion
        self.prioridad_texto = prioridad.lower()
        self.prioridad_valor = self.PRIORIDADES.get(self.prioridad_texto, 0)
        self.fecha_vencimiento = fecha_vencimiento

    def __repr__(self):
        return (f"Tarea(id={self.id}, desc='{self.descripcion}', "
                f"prioridad={self.prioridad_texto}, vence={self.fecha_vencimiento})")


class MaxHeap:
    """
    Montículo binario tipo Max-Heap para gestionar tareas por prioridad.
    El elemento con mayor prioridad_valor siempre está en la raíz (índice 0).
    """

    def __init__(self):
        self.heap = []  # lista de objetos Tarea

    # ---------- Métodos auxiliares de índices ----------
    def _padre(self, i):
        return (i - 1) // 2

    def _hijo_izquierdo(self, i):
        return 2 * i + 1

    def _hijo_derecho(self, i):
        return 2 * i + 2

    def _intercambiar(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def esta_vacio(self):
        return len(self.heap) == 0

    def tamano(self):
        return len(self.heap)

    # ---------- Inserción ----------
    def insertar(self, tarea: Tarea):
        """
        Inserta una nueva tarea en el heap.
        Paso 1: agregar al final del arreglo.
        Paso 2: "burbujear hacia arriba" (sift-up) mientras sea mayor
                que su padre, para restaurar la propiedad de max-heap.
        Complejidad: O(log n)
        """
        self.heap.append(tarea)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, i):
        while i > 0:
            padre = self._padre(i)
            if self.heap[i].prioridad_valor > self.heap[padre].prioridad_valor:
                self._intercambiar(i, padre)
                i = padre
            else:
                break

    # ---------- Extracción del máximo ----------
    def extraer_maximo(self):
        """
        Extrae y retorna la tarea de mayor prioridad (la raíz).
        Paso 1: guardar la raíz para retornarla.
        Paso 2: mover el último elemento a la raíz.
        Paso 3: "hundir hacia abajo" (sift-down) el nuevo elemento
                de la raíz para restaurar la propiedad de max-heap.
        Complejidad: O(log n)
        """
        if self.esta_vacio():
            return None

        maximo = self.heap[0]
        ultimo = self.heap.pop()  # quita y retorna el último elemento

        if not self.esta_vacio():
            self.heap[0] = ultimo
            self._sift_down(0)

        return maximo

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            izq = self._hijo_izquierdo(i)
            der = self._hijo_derecho(i)
            mayor = i

            if izq < n and self.heap[izq].prioridad_valor > self.heap[mayor].prioridad_valor:
                mayor = izq
            if der < n and self.heap[der].prioridad_valor > self.heap[mayor].prioridad_valor:
                mayor = der

            if mayor != i:
                self._intercambiar(i, mayor)
                i = mayor
            else:
                break

    def ver_maximo(self):
        """Retorna la tarea de mayor prioridad SIN eliminarla. O(1)"""
        return self.heap[0] if not self.esta_vacio() else None

    def obtener_todas(self):
        """Retorna una copia de todas las tareas en el heap (sin orden garantizado)."""
        return list(self.heap)

    # ---------- Eliminación de un elemento arbitrario (por id) ----------
    def eliminar_por_id(self, id_tarea):
        """
        Elimina una tarea específica del heap por su id (no necesariamente
        la de mayor prioridad). Se usa cuando el usuario marca cualquier
        tarea como completada, no solo la más urgente.

        Procedimiento:
        1. Buscar el índice de la tarea (O(n), el heap no está ordenado por id).
        2. Reemplazarla por el último elemento del arreglo.
        3. Restaurar la propiedad de heap con sift-up o sift-down.

        Complejidad: O(n) por la búsqueda + O(log n) por el reajuste.
        """
        indice = None
        for i, tarea in enumerate(self.heap):
            if tarea.id == id_tarea:
                indice = i
                break

        if indice is None:
            return None  # la tarea no está en el heap

        tarea_eliminada = self.heap[indice]
        ultimo_indice = len(self.heap) - 1

        self._intercambiar(indice, ultimo_indice)
        self.heap.pop()

        if indice < len(self.heap):
            padre = self._padre(indice)
            if indice > 0 and self.heap[indice].prioridad_valor > self.heap[padre].prioridad_valor:
                self._sift_up(indice)
            else:
                self._sift_down(indice)

        return tarea_eliminada


# ---------- Pruebas rápidas (se puede correr directamente este archivo) ----------
if __name__ == "__main__":
    heap = MaxHeap()

    t1 = Tarea(101, "Estudiar para el examen", "Alta", "2026-07-10")
    t2 = Tarea(102, "Comprar útiles escolares", "Media", "2026-07-12")
    t3 = Tarea(103, "Revisar correos electrónicos", "Baja", "2026-07-09")

    heap.insertar(t1)
    heap.insertar(t2)
    heap.insertar(t3)

    print("Tarea más prioritaria:", heap.ver_maximo())
    print("Extraída:", heap.extraer_maximo())
    print("Siguiente más prioritaria:", heap.ver_maximo())
