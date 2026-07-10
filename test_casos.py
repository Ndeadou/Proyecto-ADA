"""
Módulo: test_casos.py
-----------------------
Casos de prueba formales del sistema, según el enunciado:

    1. Prueba de inserción
    2. Prueba de eliminación
    3. Prueba de indexación
    4. Prueba de equilibrio (rebalanceo del AVL)

Para ejecutar todas las pruebas:
    python -m unittest test_casos.py -v
"""

import time
import unittest

from gestor_tareas import GestorTareas
from avl import ArbolAVL
from heap import Tarea


class PruebaInsercion(unittest.TestCase):
    """
    Ingresar múltiples tareas con diferentes prioridades y
    verificar el orden de extracción.
    """

    def setUp(self):
        self.gestor = GestorTareas()

    def test_insercion_multiple_y_orden_de_extraccion(self):
        self.gestor.agregar_tarea("Tarea baja", "Baja", "2026-08-01", id_tarea=1)
        self.gestor.agregar_tarea("Tarea alta", "Alta", "2026-08-02", id_tarea=2)
        self.gestor.agregar_tarea("Tarea media", "Media", "2026-08-03", id_tarea=3)

        # Se insertaron 3 tareas
        self.assertEqual(self.gestor.cantidad_tareas(), 3)

        # El orden de extracción debe ser: Alta, Media, Baja
        primera = self.gestor.completar_tarea_mas_prioritaria()
        segunda = self.gestor.completar_tarea_mas_prioritaria()
        tercera = self.gestor.completar_tarea_mas_prioritaria()

        self.assertEqual(primera.prioridad_texto, "alta")
        self.assertEqual(segunda.prioridad_texto, "media")
        self.assertEqual(tercera.prioridad_texto, "baja")

    def test_insercion_actualiza_ambas_estructuras(self):
        tarea = self.gestor.agregar_tarea("Tarea de prueba", "Alta", "2026-08-01", id_tarea=1)
        # Debe existir tanto en el heap como en el AVL
        self.assertIn(tarea, self.gestor.heap.obtener_todas())
        self.assertIsNotNone(self.gestor.avl.buscar(1))


class PruebaEliminacion(unittest.TestCase):
    """
    Extraer elementos del montículo y asegurarse de que la
    estructura se mantiene correctamente.
    """

    def setUp(self):
        self.gestor = GestorTareas()
        self.gestor.agregar_tarea("A", "Alta", "2026-08-01", id_tarea=1)
        self.gestor.agregar_tarea("B", "Media", "2026-08-02", id_tarea=2)
        self.gestor.agregar_tarea("C", "Baja", "2026-08-03", id_tarea=3)

    def test_eliminar_tarea_mas_prioritaria(self):
        tarea = self.gestor.completar_tarea_mas_prioritaria()
        self.assertEqual(tarea.id, 1)
        self.assertEqual(self.gestor.cantidad_tareas(), 2)
        # Ya no debe estar en el AVL
        self.assertIsNone(self.gestor.buscar_tarea(1))

    def test_eliminar_tarea_arbitraria_no_prioritaria(self):
        # Eliminar la tarea con id=3 (Baja), que NO es la más prioritaria
        eliminada = self.gestor.eliminar_tarea(3)
        self.assertEqual(eliminada.id, 3)
        self.assertEqual(self.gestor.cantidad_tareas(), 2)

        # La tarea más prioritaria debe seguir siendo la de id=1 (Alta)
        self.assertEqual(self.gestor.obtener_tarea_mas_prioritaria().id, 1)

        # Verificar que el heap sigue siendo un heap válido (propiedad de max-heap)
        self.assertTrue(self._es_max_heap_valido(self.gestor.heap.heap))

    def test_eliminar_todos_mantiene_heap_valido(self):
        # Extraer todas las tareas una por una y verificar la estructura en cada paso
        while not self.gestor.heap.esta_vacio():
            self.gestor.completar_tarea_mas_prioritaria()
            self.assertTrue(self._es_max_heap_valido(self.gestor.heap.heap))

        self.assertEqual(self.gestor.cantidad_tareas(), 0)

    @staticmethod
    def _es_max_heap_valido(lista_heap):
        """Verifica que cada padre sea >= que sus hijos, en toda la lista."""
        n = len(lista_heap)
        for i in range(n):
            izq, der = 2 * i + 1, 2 * i + 2
            if izq < n and lista_heap[i].prioridad_valor < lista_heap[izq].prioridad_valor:
                return False
            if der < n and lista_heap[i].prioridad_valor < lista_heap[der].prioridad_valor:
                return False
        return True


class PruebaIndexacion(unittest.TestCase):
    """
    Buscar objetos aleatorios en el árbol AVL y confirmar
    tiempos de respuesta eficientes (O(log n)).
    """

    def setUp(self):
        self.gestor = GestorTareas()
        # Insertamos 1000 tareas para tener una muestra significativa
        for i in range(1, 1001):
            self.gestor.agregar_tarea(f"Tarea {i}", "Media", "2026-08-01", id_tarea=i)

    def test_busqueda_de_elementos_existentes(self):
        for id_buscado in [1, 250, 500, 750, 1000]:
            tarea = self.gestor.buscar_tarea(id_buscado)
            self.assertIsNotNone(tarea)
            self.assertEqual(tarea.id, id_buscado)

    def test_busqueda_de_elemento_inexistente(self):
        self.assertIsNone(self.gestor.buscar_tarea(99999))

    def test_tiempo_de_busqueda_eficiente(self):
        """
        Con 1000 elementos, la búsqueda en el AVL (O(log n)) debe
        tomar una fracción de milisegundo. Se usa un límite generoso
        (10 ms) para evitar falsos negativos por variabilidad de la máquina.
        """
        inicio = time.perf_counter()
        self.gestor.buscar_tarea(500)
        duracion = time.perf_counter() - inicio

        self.assertLess(duracion, 0.01, "La búsqueda tardó más de lo esperado para O(log n)")

    def test_altura_del_arbol_es_logaritmica(self):
        """
        Con 1000 elementos, la altura del AVL debe ser cercana a
        log2(1000) ≈ 10, y NUNCA cercana a 1000 (que sería un BST degenerado).
        """
        altura = self.gestor.avl.raiz.altura
        self.assertLess(altura, 15, "La altura del AVL es demasiado grande; posible desbalance")


class PruebaEquilibrio(unittest.TestCase):
    """
    Insertar una secuencia desbalanceada en el árbol AVL y
    verificar que se reestructura adecuadamente.
    """

    def test_rotacion_ll(self):
        # Insertar en orden descendente fuerza rotaciones LL
        avl = ArbolAVL()
        for i in [30, 20, 10]:
            avl.insertar(Tarea(i, f"t{i}", "Media", "2026-08-01"))
        # Tras la rotación, 20 debe quedar como raíz
        self.assertEqual(avl.raiz.tarea.id, 20)
        self.assertEqual(avl.raiz.izquierdo.tarea.id, 10)
        self.assertEqual(avl.raiz.derecho.tarea.id, 30)

    def test_rotacion_rr(self):
        # Insertar en orden ascendente fuerza rotaciones RR
        avl = ArbolAVL()
        for i in [10, 20, 30]:
            avl.insertar(Tarea(i, f"t{i}", "Media", "2026-08-01"))
        self.assertEqual(avl.raiz.tarea.id, 20)
        self.assertEqual(avl.raiz.izquierdo.tarea.id, 10)
        self.assertEqual(avl.raiz.derecho.tarea.id, 30)

    def test_rotacion_lr(self):
        # 30, 10, 20 -> fuerza rotación izquierda-derecha
        avl = ArbolAVL()
        for i in [30, 10, 20]:
            avl.insertar(Tarea(i, f"t{i}", "Media", "2026-08-01"))
        self.assertEqual(avl.raiz.tarea.id, 20)
        self.assertEqual(avl.raiz.izquierdo.tarea.id, 10)
        self.assertEqual(avl.raiz.derecho.tarea.id, 30)

    def test_rotacion_rl(self):
        # 10, 30, 20 -> fuerza rotación derecha-izquierda
        avl = ArbolAVL()
        for i in [10, 30, 20]:
            avl.insertar(Tarea(i, f"t{i}", "Media", "2026-08-01"))
        self.assertEqual(avl.raiz.tarea.id, 20)
        self.assertEqual(avl.raiz.izquierdo.tarea.id, 10)
        self.assertEqual(avl.raiz.derecho.tarea.id, 30)

    def test_secuencia_desbalanceada_grande_mantiene_altura_log(self):
        """
        Insertar una secuencia grande y estrictamente ascendente
        (el peor caso posible para un BST normal) y confirmar que
        el AVL se mantiene balanceado.
        """
        avl = ArbolAVL()
        n = 100
        for i in range(1, n + 1):
            avl.insertar(Tarea(i, f"t{i}", "Media", "2026-08-01"))

        # log2(100) ≈ 6.64, la altura real de un AVL nunca supera ~1.44*log2(n)
        self.assertLessEqual(avl.raiz.altura, 10)

        # El recorrido in-order debe seguir dando la secuencia ordenada correcta
        ids_en_orden = [t.id for t in avl.in_order()]
        self.assertEqual(ids_en_orden, list(range(1, n + 1)))

    def test_factor_de_equilibrio_nunca_excede_uno(self):
        """Tras muchas inserciones, ningún nodo debe tener |factor de equilibrio| > 1."""
        avl = ArbolAVL()
        import random
        valores = list(range(1, 201))
        random.shuffle(valores)
        for v in valores:
            avl.insertar(Tarea(v, f"t{v}", "Media", "2026-08-01"))

        self.assertTrue(self._verificar_balance(avl, avl.raiz))

    def _verificar_balance(self, avl, nodo):
        if nodo is None:
            return True
        factor = avl._factor_equilibrio(nodo)
        if abs(factor) > 1:
            return False
        return self._verificar_balance(avl, nodo.izquierdo) and self._verificar_balance(avl, nodo.derecho)


if __name__ == "__main__":
    unittest.main(verbosity=2)
