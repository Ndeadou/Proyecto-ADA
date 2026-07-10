"""
Módulo: gui.py
---------------
Interfaz gráfica (tkinter) para el sistema de gestión de tareas.
Conecta la interfaz visual con la lógica de GestorTareas
(heap + árbol AVL).

Para ejecutar:
    python gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from gestor_tareas import GestorTareas


class AplicacionTareas(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Tareas - Heap + AVL")
        self.geometry("650x500")
        self.resizable(False, False)

        self.gestor = GestorTareas()

        self._crear_widgets()
        self._actualizar_lista()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _crear_widgets(self):
        # ---------- Formulario para agregar tareas ----------
        marco_formulario = ttk.LabelFrame(self, text="Agregar nueva tarea")
        marco_formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(marco_formulario, text="Descripción:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_descripcion = ttk.Entry(marco_formulario, width=40)
        self.entrada_descripcion.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco_formulario, text="Prioridad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_prioridad = ttk.Combobox(
            marco_formulario, values=["Alta", "Media", "Baja"], state="readonly", width=15
        )
        self.combo_prioridad.set("Media")
        self.combo_prioridad.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(marco_formulario, text="Fecha vencimiento (YYYY-MM-DD):").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.entrada_fecha = ttk.Entry(marco_formulario, width=20)
        self.entrada_fecha.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        boton_agregar = ttk.Button(marco_formulario, text="Agregar tarea", command=self._agregar_tarea)
        boton_agregar.grid(row=3, column=0, columnspan=2, pady=10)

        # ---------- Panel de acciones ----------
        marco_acciones = ttk.LabelFrame(self, text="Acciones")
        marco_acciones.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            marco_acciones, text="Ver tarea más prioritaria", command=self._ver_mas_prioritaria
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(
            marco_acciones, text="Completar tarea más prioritaria", command=self._completar_mas_prioritaria
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco_acciones, text="Buscar/Eliminar por ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_id = ttk.Entry(marco_acciones, width=10)
        self.entrada_id.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(marco_acciones, text="Buscar", command=self._buscar_por_id).grid(
            row=1, column=2, padx=5, pady=5
        )
        ttk.Button(marco_acciones, text="Eliminar", command=self._eliminar_por_id).grid(
            row=1, column=3, padx=5, pady=5
        )

        # ---------- Lista de tareas (ordenadas por id, vía AVL in-order) ----------
        marco_lista = ttk.LabelFrame(self, text="Tareas (ordenadas por ID - recorrido in-order del AVL)")
        marco_lista.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("id", "descripcion", "prioridad", "vencimiento")
        self.tabla = ttk.Treeview(marco_lista, columns=columnas, show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("prioridad", text="Prioridad")
        self.tabla.heading("vencimiento", text="Vencimiento")

        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("descripcion", width=280)
        self.tabla.column("prioridad", width=100, anchor="center")
        self.tabla.column("vencimiento", width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------- Barra de estado ----------
        self.texto_estado = tk.StringVar(value="Listo.")
        ttk.Label(self, textvariable=self.texto_estado, relief="sunken", anchor="w").pack(
            fill="x", side="bottom"
        )

    # ------------------------------------------------------------------
    # Manejadores de eventos (conectan la GUI con GestorTareas)
    # ------------------------------------------------------------------
    def _agregar_tarea(self):
        descripcion = self.entrada_descripcion.get().strip()
        prioridad = self.combo_prioridad.get()
        fecha = self.entrada_fecha.get().strip()

        if not descripcion or not fecha:
            messagebox.showwarning("Datos incompletos", "Por favor completa descripción y fecha.")
            return

        tarea = self.gestor.agregar_tarea(descripcion, prioridad, fecha)
        self.texto_estado.set(f"Tarea agregada: id={tarea.id}")

        self.entrada_descripcion.delete(0, tk.END)
        self.entrada_fecha.delete(0, tk.END)

        self._actualizar_lista()

    def _ver_mas_prioritaria(self):
        tarea = self.gestor.obtener_tarea_mas_prioritaria()
        if tarea is None:
            messagebox.showinfo("Cola vacía", "No hay tareas pendientes.")
            return
        messagebox.showinfo(
            "Tarea más prioritaria",
            f"ID: {tarea.id}\nDescripción: {tarea.descripcion}\n"
            f"Prioridad: {tarea.prioridad_texto}\nVence: {tarea.fecha_vencimiento}",
        )

    def _completar_mas_prioritaria(self):
        tarea = self.gestor.completar_tarea_mas_prioritaria()
        if tarea is None:
            messagebox.showinfo("Cola vacía", "No hay tareas pendientes.")
            return
        self.texto_estado.set(f"Tarea completada: id={tarea.id} - {tarea.descripcion}")
        self._actualizar_lista()

    def _buscar_por_id(self):
        texto_id = self.entrada_id.get().strip()
        if not texto_id.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un número de ID válido.")
            return

        tarea = self.gestor.buscar_tarea(int(texto_id))
        if tarea is None:
            messagebox.showinfo("No encontrada", f"No existe una tarea con id={texto_id}.")
        else:
            messagebox.showinfo(
                "Tarea encontrada",
                f"ID: {tarea.id}\nDescripción: {tarea.descripcion}\n"
                f"Prioridad: {tarea.prioridad_texto}\nVence: {tarea.fecha_vencimiento}",
            )

    def _eliminar_por_id(self):
        texto_id = self.entrada_id.get().strip()
        if not texto_id.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un número de ID válido.")
            return

        tarea = self.gestor.eliminar_tarea(int(texto_id))
        if tarea is None:
            messagebox.showinfo("No encontrada", f"No existe una tarea con id={texto_id}.")
        else:
            self.texto_estado.set(f"Tarea eliminada: id={tarea.id}")
        self._actualizar_lista()

    def _actualizar_lista(self):
        """Refresca la tabla mostrando todas las tareas ordenadas por id (AVL in-order)."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for tarea in self.gestor.listar_todas_por_id():
            self.tabla.insert(
                "", tk.END,
                values=(tarea.id, tarea.descripcion, tarea.prioridad_texto, tarea.fecha_vencimiento),
            )


if __name__ == "__main__":
    app = AplicacionTareas()
    app.mainloop()
