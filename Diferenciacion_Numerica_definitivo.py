import tkinter as tk
from tkinter import ttk
import math

# ------------------------ THEME (Cyber-Neón) ------------------------
BG = "#020205"         # fondo oscuro
PANEL = "#28383D"      # panel oscuro ligeramente distinto
NEON = "#169CA3"       # turquesa neón-
ACCENT = "#19ABCF"     # acento claro
TEXT = "#E6F7FB"       # texto claro
INPUT_BG = "#07101A"   # fondo inputs
INPUT_FG = TEXT

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUB = ("Segoe UI", 12)
FONT_INPUT = ("Segoe UI", 12)
FONT_BIG = ("Segoe UI", 18, "bold")

SAFE_MATH = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
    "pi": math.pi, "e": math.e, "pow": pow, "abs": abs
}


# ------------------------ UTIL - CENTRAR Toplevel ------------------------
def centrar_ventana(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


# ------------------------ VENTANAS MODALES TEMA ------------------------
def mostrar_error(parent, texto):
    dlg = tk.Toplevel(parent)
    dlg.title("Error")
    dlg.configure(bg=PANEL)
    dlg.resizable(False, False)
    centrar_ventana(dlg, 520, 220)

    lbl = tk.Label(dlg, text="Error", font=FONT_BIG, bg=PANEL, fg=NEON)
    lbl.pack(pady=(18, 6))
    msg = tk.Label(dlg, text=texto, font=FONT_SUB, bg=PANEL, fg=TEXT, wraplength=480, justify="center")
    msg.pack(pady=(0, 18), padx=10)

    btn = ttk.Button(dlg, text="Cerrar", command=dlg.destroy)
    btn.pack(pady=10)
    btn.focus_set()
    dlg.transient(parent)
    dlg.grab_set()
    return dlg


def mostrar_resultado(parent, texto):
    dlg = tk.Toplevel(parent)
    dlg.title("Resultado")
    dlg.configure(bg=PANEL)
    dlg.resizable(False, False)
    centrar_ventana(dlg, 620, 300)

    tk.Label(dlg, text="Resultado", font=FONT_BIG, bg=PANEL, fg=NEON).pack(pady=(18, 6))
    tk.Label(dlg, text=texto, font=("Segoe UI", 16), bg=PANEL, fg=TEXT, wraplength=580, justify="center").pack(pady=(0, 18), padx=12)

    ttk.Button(dlg, text="Cerrar", command=dlg.destroy).pack(pady=10)
    dlg.transient(parent)
    dlg.grab_set()
    return dlg


# ------------------------ APLICACIÓN (UNA VENTANA, MULTIPLES PANTALLAS) ------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Diferenciación Numérica — Cyber-Neón")
        root.configure(bg=BG)
        root.geometry("760x620")
        root.resizable(False, False)

        # ttk styling (botones minimalistas con acento)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), foreground="white", padding=8)
        style.map("TButton", background=[("active", ACCENT), ("!disabled", NEON)])

        self.filas = []
        self.delta = None
        self.n = 0

        # contenedor principal
        self.container = tk.Frame(root, bg=BG)
        self.container.pack(fill="both", expand=True)

        # crear pantallas
        self.pantallas = {}
        self._crear_pantalla_inicial()
        self._crear_pantalla_x()
        self._crear_pantalla_y()
        self._crear_pantalla_metodos()
        self._crear_pantalla_indice()

        # iniciar en pantalla inicial
        self.mostrar("inicio")

    # ---------------- pantalla helper ----------------
    def mostrar(self, name):
        for p in self.pantallas.values():
            p.pack_forget()
        self.pantallas[name].pack(fill="both", expand=True)

    # ---------------- pantalla 1: ingresar n ----------------
    def _crear_pantalla_inicial(self):
        f = tk.Frame(self.container, bg=BG)
        self.pantallas["inicio"] = f

        title = tk.Label(f, text="Diferenciación Numérica", font=FONT_TITLE, bg=BG, fg=NEON)
        title.pack(pady=(30, 8))

        subtitle = tk.Label(f, text="Pantalla 1 — Ingrese cantidad de puntos (n ≥ 3)", font=FONT_SUB, bg=BG, fg=TEXT)
        subtitle.pack(pady=(0, 20))

        box = tk.Frame(f, bg=PANEL, bd=0, padx=20, pady=20)
        box.pack(pady=10)

        tk.Label(box, text="Número de puntos (n):", font=FONT_SUB, bg=PANEL, fg=TEXT).pack(pady=(6,6))
        self.entry_n = tk.Entry(box, font=FONT_INPUT, width=8, bg=INPUT_BG, fg=INPUT_FG, justify="center", bd=0)
        self.entry_n.pack(pady=(0,12))
        self.entry_n.bind("<Return>", lambda e: self._on_n_continue())

        btn = ttk.Button(box, text="Continuar", command=self._on_n_continue)
        btn.pack(pady=10)

        note = tk.Label(f, text="Presiona ENTER para avanzar entre campos.", font=("Segoe UI", 10), bg=BG, fg=ACCENT)
        note.pack(pady=8)

    def _on_n_continue(self):
        try:
            n = int(self.entry_n.get())
        except:
            mostrar_error(self.root, "Ingrese un número entero válido para la cantidad de puntos (n).")
            return
        if n < 3:
            mostrar_error(self.root, "Se requieren al menos 3 puntos (n ≥ 3).")
            return
        self.n = n
        self.filas = [[0.0, 0.0] for _ in range(self.n)]
        # limpiar pantalla y mostrar pantalla X
        self._limpiar_entradas_x()
        self.mostrar("x")

    # ---------------- pantalla 2: ingresar X ----------------
    def _crear_pantalla_x(self):
        f = tk.Frame(self.container, bg=BG)
        self.pantallas["x"] = f

        title = tk.Label(f, text="Ingresar valores de X", font=FONT_TITLE, bg=BG, fg=NEON)
        title.pack(pady=(16,6))
        subtitle = tk.Label(f, text="Pantalla 2 — X deben estar igualmente espaciados", font=FONT_SUB, bg=BG, fg=TEXT)
        subtitle.pack(pady=(0,12))

        box = tk.Frame(f, bg=PANEL, padx=18, pady=14)
        box.pack(pady=6, padx=12, fill="x")

        self.x_inputs_container = tk.Frame(box, bg=PANEL)
        self.x_inputs_container.pack()

        # botones centrados
        btns = tk.Frame(f, bg=BG)
        btns.pack(pady=12)
        ttk.Button(btns, text="Volver", command=lambda: self.mostrar("inicio")).pack(side="left", padx=8)
        ttk.Button(btns, text="Validar X", command=self._validar_x).pack(side="left", padx=8)

    def _limpiar_entradas_x(self):
        # destruir antiguos widgets y crear entradas nuevas
        for w in self.x_inputs_container.winfo_children():
            w.destroy()
        self.x_entries = []
        for i in range(self.n):
            row = tk.Frame(self.x_inputs_container, bg=PANEL)
            row.pack(pady=4, padx=6, fill="x")
            lbl = tk.Label(row, text=f"x[{i+1}]:", font=FONT_SUB, width=8, anchor="e", bg=PANEL, fg=TEXT)
            lbl.pack(side="left")
            ent = tk.Entry(row, font=FONT_INPUT, bg=INPUT_BG, fg=INPUT_FG, bd=0, justify="center")
            ent.pack(side="left", padx=6, ipadx=6, fill="x", expand=True)
            # bind para avanzar con Enter
            ent.bind("<Return>", lambda e, idx=i: self._x_enter(idx))
            self.x_entries.append(ent)
        # focus primero
        if self.x_entries:
            self.root.after(50, lambda: self.x_entries[0].focus_set())

    def _x_enter(self, idx):
        try:
            val = float(self.x_entries[idx].get())
            self.filas[idx][0] = val
        except:
            # si no es numérico mostramos error pero dejamos foco
            mostrar_error(self.root, f"Valor inválido en x[{idx+1}]. Debe ser numérico (decimal permitido).")
            return
        if idx < self.n - 1:
            self.x_entries[idx + 1].focus_set()
        else:
            # último -> validar automáticamente
            self._validar_x()

    def _validar_x(self):
        # leer todos x (si no se presionó Enter en alguno)
        try:
            for i in range(self.n):
                self.filas[i][0] = float(self.x_entries[i].get())
        except:
            mostrar_error(self.root, "Todos los X deben ser números (decimales permitidos).")
            return

        # comprobar espaciado constante
        delta = self.filas[1][0] - self.filas[0][0]
        for i in range(2, self.n):
            if abs((self.filas[i][0] - self.filas[i - 1][0]) - delta) > 1e-12:
                mostrar_error(self.root, f"X no igualmente espaciados. Se esperaba diferencia {delta:.6g}.")
                return
        self.delta = delta
        # avanzar a Y y limpiar su pantalla
        self._limpiar_entradas_y()
        self.mostrar("y")

    # ---------------- pantalla 3: ingresar Y ----------------
    def _crear_pantalla_y(self):
        f = tk.Frame(self.container, bg=BG)
        self.pantallas["y"] = f

        title = tk.Label(f, text="Ingresar valores de Y o usar f(x)", font=FONT_TITLE, bg=BG, fg=NEON)
        title.pack(pady=(16,6))
        subtitle = tk.Label(f, text="Pantalla 3 — Ingrese Y manualmente o ingrese f(x) y presione ENTER", font=FONT_SUB, bg=BG, fg=TEXT)
        subtitle.pack(pady=(0,10))

        box = tk.Frame(f, bg=PANEL, padx=18, pady=14)
        box.pack(pady=6, padx=12, fill="x")

        # opcion funcion
        func_frame = tk.Frame(box, bg=PANEL)
        func_frame.pack(fill="x", pady=6)
        tk.Label(func_frame, text="f(x) = ", font=FONT_SUB, bg=PANEL, fg=TEXT).pack(side="left")
        self.func_entry = tk.Entry(func_frame, font=FONT_INPUT, bg=INPUT_BG, fg=INPUT_FG, bd=0)
        self.func_entry.pack(side="left", fill="x", expand=True, padx=6)
        self.func_entry.bind("<Return>", lambda e: self._evaluar_funcion())

        tk.Label(box, text="-- O ingrese Y manualmente abajo --", bg=PANEL, fg=ACCENT, font=("Segoe UI", 10, "italic")).pack(pady=6)

        self.y_inputs_container = tk.Frame(box, bg=PANEL)
        self.y_inputs_container.pack(fill="x")
        # botones
        btns = tk.Frame(f, bg=BG)
        btns.pack(pady=12)
        ttk.Button(btns, text="Volver (X)", command=lambda: self.mostrar("x")).pack(side="left", padx=8)
        ttk.Button(btns, text="Validar Y", command=self._validar_y).pack(side="left", padx=8)

    def _limpiar_entradas_y(self):
        for w in self.y_inputs_container.winfo_children():
            w.destroy()
        self.y_entries = []
        for i in range(self.n):
            row = tk.Frame(self.y_inputs_container, bg=PANEL)
            row.pack(pady=4, padx=6, fill="x")
            lbl = tk.Label(row, text=f"y[{i+1}]:", font=FONT_SUB, width=8, anchor="e", bg=PANEL, fg=TEXT)
            lbl.pack(side="left")
            ent = tk.Entry(row, font=FONT_INPUT, bg=INPUT_BG, fg=INPUT_FG, bd=0, justify="center")
            ent.pack(side="left", padx=6, ipadx=6, fill="x", expand=True)
            ent.bind("<Return>", lambda e, idx=i: self._y_enter(idx))
            self.y_entries.append(ent)
        # focus first
        if self.y_entries:
            self.root.after(50, lambda: self.y_entries[0].focus_set())

    def _y_enter(self, idx):
        try:
            val = float(self.y_entries[idx].get())
            self.filas[idx][1] = val
        except:
            mostrar_error(self.root, f"Valor inválido en y[{idx+1}]. Debe ser numérico.")
            return
        if idx < self.n - 1:
            self.y_entries[idx + 1].focus_set()
        else:
            self._validar_y()

    def _evaluar_funcion(self):
        expr = self.func_entry.get().strip()
        if not expr:
            mostrar_error(self.root, "Ingrese una expresión válida para f(x) o ingrese Y manualmente.")
            return
        # evaluar función con seguridad: sin __builtins__
        try:
            for i in range(self.n):
                x = float(self.filas[i][0])
                # eval con globals limitado y locals con x + math funcs
                val = eval(expr, {"__builtins__": None}, {**SAFE_MATH, "x": x})
                self.filas[i][1] = float(val)
        except Exception as e:
            mostrar_error(self.root, f"Error al evaluar f(x): {e}")
            return
        # rellenar campos y mostrar pantalla de métodos
        self._limpiar_entradas_y()
        for i in range(self.n):
            # crear visualmente los valores en las entradas (opcional)
            ent = tk.Entry(self.y_inputs_container, font=FONT_INPUT, bg=INPUT_BG, fg=INPUT_FG, bd=0, justify="center")
            ent.pack(pady=3, fill="x")
            ent.insert(0, str(self.filas[i][1]))
            ent.config(state="disabled")
            self.y_entries.append(ent)
        self.mostrar("metodos")

    def _validar_y(self):
        try:
            for i in range(self.n):
                self.filas[i][1] = float(self.y_entries[i].get())
        except Exception:
            mostrar_error(self.root, "Todos los Y deben ser números (decimales permitidos).")
            return
        # avanzar
        self.mostrar("metodos")

    # ---------------- pantalla 4: metodos ----------------
    def _crear_pantalla_metodos(self):
        f = tk.Frame(self.container, bg=BG)
        self.pantallas["metodos"] = f

        tk.Label(f, text="Seleccionar método", font=FONT_TITLE, bg=BG, fg=NEON).pack(pady=18)
        tk.Label(f, text="Pantalla 4 — Elija un esquema para calcular la derivada", font=FONT_SUB, bg=BG, fg=TEXT).pack(pady=(0,10))

        box = tk.Frame(f, bg=PANEL, padx=20, pady=16)
        box.pack(pady=6)

        # botones grandes centrados
        ttk.Button(box, text="1) Igualmente espaciado (central 3 puntos)", command=lambda: self._pedir_indice(1)).pack(fill="x", pady=6)
        ttk.Button(box, text="2) Extremo izquierdo (fórmula hacia adelante)", command=lambda: self._pedir_indice(2)).pack(fill="x", pady=6)
        ttk.Button(box, text="3) Central (diferencia central)", command=lambda: self._pedir_indice(3)).pack(fill="x", pady=6)
        ttk.Button(box, text="4) Extremo derecho (fórmula hacia atrás)", command=lambda: self._pedir_indice(4)).pack(fill="x", pady=6)

        ttk.Button(f, text="Volver (Y)", command=lambda: self.mostrar("y")).pack(pady=12)

    # ---------------- pantalla 5: indice ----------------
    def _crear_pantalla_indice(self):
        f = tk.Frame(self.container, bg=BG)
        self.pantallas["indice"] = f

        tk.Label(f, text="Ingrese índice i", font=FONT_TITLE, bg=BG, fg=NEON).pack(pady=18)
        tk.Label(f, text="Pantalla 5 — Indice entre 1 y n", font=FONT_SUB, bg=BG, fg=TEXT).pack(pady=(0,10))

        box = tk.Frame(f, bg=PANEL, padx=20, pady=14)
        box.pack(pady=6)
        tk.Label(box, text="Índice i (1..n):", font=FONT_SUB, bg=PANEL, fg=TEXT).pack(pady=6)
        self.entry_i = tk.Entry(box, font=FONT_INPUT, bg=INPUT_BG, fg=INPUT_FG, bd=0, justify="center")
        self.entry_i.pack(pady=6)
        self.entry_i.bind("<Return>", lambda e: self._calcular_derivada())

        btns = tk.Frame(f, bg=BG)
        btns.pack(pady=12)
        ttk.Button(btns, text="Volver (Métodos)", command=lambda: self.mostrar("metodos")).pack(side="left", padx=8)
        ttk.Button(btns, text="Calcular", command=self._calcular_derivada).pack(side="left", padx=8)

        # guardará el método pedido
        self._metodo_pedido = None

    def _pedir_indice(self, metodo):
        # guardar metodo y mostrar pantalla indice
        self._metodo_pedido = metodo
        # limpiar campo
        self.entry_i.delete(0, "end")
        self.mostrar("indice")
        self.entry_i.focus_set()

    def _calcular_derivada(self):
        s = self.entry_i.get().strip()
        if not s:
            mostrar_error(self.root, "Ingrese un índice i entre 1 y n.")
            return
        try:
            i = int(s)
        except:
            mostrar_error(self.root, "Índice inválido. Debe ser entero.")
            return
        if not (1 <= i <= self.n):
            mostrar_error(self.root, f"Índice fuera de rango. Debe ser 1 ≤ i ≤ {self.n}.")
            return

        i0 = i - 1
        metodo = self._metodo_pedido
        der = None

        try:
            if metodo == 1:  # igualmente espaciado (central 3 puntos)
                if i0 == 0 or i0 == self.n - 1:
                    mostrar_error(self.root, "No se puede aplicar en extremos; requiere 3 puntos.")
                    return
                der = (self.filas[i0 + 1][1] - self.filas[i0 - 1][1]) / (2 * self.delta)

            elif metodo == 2:  # extremo izquierdo (hacia adelante)
                if i0 > self.n - 3:
                    mostrar_error(self.root, "No hay suficientes puntos a la derecha para extremo izquierdo.")
                    return
                y0, y1, y2 = self.filas[i0][1], self.filas[i0 + 1][1], self.filas[i0 + 2][1]
                der = (-1.5 * y0 + 2 * y1 - 0.5 * y2) / self.delta

            elif metodo == 3:  # central
                if i0 == 0 or i0 == self.n - 1:
                    mostrar_error(self.root, "No aplica en extremos.")
                    return
                der = (self.filas[i0 + 1][1] - self.filas[i0 - 1][1]) / (2 * self.delta)

            elif metodo == 4:  # extremo derecho (hacia atrás)
                if i0 < 2:
                    mostrar_error(self.root, "No hay suficientes puntos a la izquierda para extremo derecho.")
                    return
                y0, y1, y2 = self.filas[i0][1], self.filas[i0 - 1][1], self.filas[i0 - 2][1]
                der = (0.5 * y2 - 2 * y1 + 1.5 * y0) / self.delta

            else:
                mostrar_error(self.root, "Método no reconocido.")
                return
        except Exception as e:
            mostrar_error(self.root, f"Error calculando derivada: {e}")
            return

        # mostrar resultado en modal temático grande
        texto = f"f'({self.filas[i0][0]}) = {der}"
        mostrar_resultado(self.root, texto)
        # después de resultado, volver a pantalla métodos
        self.mostrar("metodos")


# --------------------------- EJECUCIÓN ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
