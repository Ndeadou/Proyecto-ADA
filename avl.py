"""
Módulo: avl.py
---------------
Implementa un Árbol AVL (Adelson-Velsky y Landis) para indexar
tareas por su ID único, garantizando búsquedas en O(log n).

Un AVL es un Árbol Binario de Búsqueda (BST) que se autobalancea:
después de cada inserción o eliminación, se revisa el factor de
equilibrio de cada nodo y, si es necesario, se aplican rotaciones
(LL, RR, LR, RL) para mantener la altura del árbol en O(log n).
"""

from heap import Tarea  # reutilizamos la clase Tarea definida en heap.py


class NodoAVL:
    """Nodo del árbol AVL. Guarda una tarea completa, indexada por tarea.id"""

    def __init__(self, tarea: Tarea):
        self.tarea = tarea
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # altura de un nodo hoja es 1


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    # ---------- Utilidades de altura y balance ----------
    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _factor_equilibrio(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    # ---------- Rotaciones ----------
    def _rotacion_derecha(self, y):
        """
        Rotación simple a la derecha (caso LL).
              y                x
             / \\              / \\
            x   T3   ---->   T1   y
           / \\                   / \\
          T1  T2                T2  T3
        """
        x = y.izquierdo
        T2 = x.derecho

        x.derecho = y
        y.izquierdo = T2

        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x  # x es la nueva raíz de este subárbol

    def _rotacion_izquierda(self, x):
        """
        Rotación simple a la izquierda (caso RR).
            x                    y
           / \\                  / \\
          T1  y      ---->      x   T3
             / \\               / \\
            T2  T3            T1  T2
        """
        y = x.derecho
        T2 = y.izquierdo

        y.izquierdo = x
        x.derecho = T2

        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y  # y es la nueva raíz de este subárbol

    # ---------- Inserción ----------
    def insertar(self, tarea: Tarea):
        """Inserta una tarea en el árbol, indexada por tarea.id. O(log n)"""
        self.raiz = self._insertar_recursivo(self.raiz, tarea)

    def _insertar_recursivo(self, nodo, tarea):
        # 1. Inserción normal de BST (por id)
        if nodo is None:
            return NodoAVL(tarea)

        if tarea.id < nodo.tarea.id:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, tarea)
        elif tarea.id > nodo.tarea.id:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, tarea)
        else:
            # id duplicado: actualizamos la tarea existente
            nodo.tarea = tarea
            return nodo

        # 2. Actualizar altura del nodo actual
        self._actualizar_altura(nodo)

        # 3. Calcular factor de equilibrio y rebalancear si hace falta
        balance = self._factor_equilibrio(nodo)

        # Caso LL
        if balance > 1 and tarea.id < nodo.izquierdo.tarea.id:
            return self._rotacion_derecha(nodo)

        # Caso RR
        if balance < -1 and tarea.id > nodo.derecho.tarea.id:
            return self._rotacion_izquierda(nodo)

        # Caso LR
        if balance > 1 and tarea.id > nodo.izquierdo.tarea.id:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)

        # Caso RL
        if balance < -1 and tarea.id < nodo.derecho.tarea.id:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)

        return nodo

    # ---------- Búsqueda ----------
    def buscar(self, id_tarea):
        """Busca una tarea por su id. Retorna la Tarea o None. O(log n)"""
        return self._buscar_recursivo(self.raiz, id_tarea)

    def _buscar_recursivo(self, nodo, id_tarea):
        if nodo is None:
            return None
        if id_tarea == nodo.tarea.id:
            return nodo.tarea
        elif id_tarea < nodo.tarea.id:
            return self._buscar_recursivo(nodo.izquierdo, id_tarea)
        else:
            return self._buscar_recursivo(nodo.derecho, id_tarea)

    # ---------- Eliminación ----------
    def eliminar(self, id_tarea):
        """Elimina una tarea por su id y rebalancea el árbol. O(log n)"""
        self.raiz = self._eliminar_recursivo(self.raiz, id_tarea)

    def _nodo_valor_minimo(self, nodo):
        """Encuentra el nodo con el id más pequeño de un subárbol (para eliminar)."""
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def _eliminar_recursivo(self, nodo, id_tarea):
        if nodo is None:
            return nodo

        # 1. Eliminación normal de BST
        if id_tarea < nodo.tarea.id:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, id_tarea)
        elif id_tarea > nodo.tarea.id:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, id_tarea)
        else:
            # Nodo encontrado: caso con 0 o 1 hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo

            # Caso con 2 hijos: buscar el sucesor in-order (mínimo del subárbol derecho)
            sucesor = self._nodo_valor_minimo(nodo.derecho)
            nodo.tarea = sucesor.tarea
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.tarea.id)

        # 2. Actualizar altura
        self._actualizar_altura(nodo)

        # 3. Rebalancear
        balance = self._factor_equilibrio(nodo)

        # Caso LL
        if balance > 1 and self._factor_equilibrio(nodo.izquierdo) >= 0:
            return self._rotacion_derecha(nodo)

        # Caso LR
        if balance > 1 and self._factor_equilibrio(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)

        # Caso RR
        if balance < -1 and self._factor_equilibrio(nodo.derecho) <= 0:
            return self._rotacion_izquierda(nodo)

        # Caso RL
        if balance < -1 and self._factor_equilibrio(nodo.derecho) > 0:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)

        return nodo

    # ---------- Recorrido in-order (para depurar / listar ordenado por id) ----------
    def in_order(self):
        resultado = []
        self._in_order_recursivo(self.raiz, resultado)
        return resultado

    def _in_order_recursivo(self, nodo, resultado):
        if nodo:
            self._in_order_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.tarea)
            self._in_order_recursivo(nodo.derecho, resultado)


# ---------- Pruebas rápidas ----------
if __name__ == "__main__":
    avl = ArbolAVL()

    t1 = Tarea(101, "Estudiar para el examen", "Alta", "2026-07-10")
    t2 = Tarea(102, "Comprar útiles escolares", "Media", "2026-07-12")
    t3 = Tarea(103, "Revisar correos electrónicos", "Baja", "2026-07-09")

    avl.insertar(t1)
    avl.insertar(t2)
    avl.insertar(t3)

    print("Búsqueda id=102:", avl.buscar(102))
    print("In-order (ordenado por id):", avl.in_order())

    avl.eliminar(102)
    print("Después de eliminar 102, búsqueda id=102:", avl.buscar(102))

    # Prueba de desbalance: insertar secuencia ascendente (fuerza rotaciones RR)
    avl2 = ArbolAVL()
    for i in [10, 20, 30, 40, 50]:
        avl2.insertar(Tarea(i, f"tarea {i}", "Media", "2026-08-01"))
    print("In-order tras secuencia ascendente (debe seguir balanceado):",
          [t.id for t in avl2.in_order()])
    print("Altura de la raíz (debe ser ~log2(5)≈3, no 5):", avl2.raiz.altura)
