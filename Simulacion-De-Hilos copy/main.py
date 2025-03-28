import tkinter as tk
import threading
import time
import random
from queue import Queue

# Configuración inicial de la ventana
root = tk.Tk()
root.title("Simulación de Hilos - Restaurante")
root.geometry("800x600")

# Variables globales
clientes_atendidos = 0
tiempo_total_espera = 0
clientes_en_espera = Queue()
pedidos_en_preparacion = Queue()
mesas_disponibles = 5
mesas_ocupadas = []
lock = threading.Lock()

# Crear un canvas para dibujar
canvas = tk.Canvas(root, width=800, height=500, bg="white")
canvas.pack()

# Coordenadas de las mesas
mesas = [
    {"x": 100, "y": 100, "estado": "disponible", "cliente_id": None},
    {"x": 300, "y": 100, "estado": "disponible", "cliente_id": None},
    {"x": 500, "y": 100, "estado": "disponible", "cliente_id": None},
    {"x": 200, "y": 300, "estado": "disponible", "cliente_id": None},
    {"x": 400, "y": 300, "estado": "disponible", "cliente_id": None},
]

# Coordenadas del cocinero
cocinero_x = 700
cocinero_y = 200

# Dibujar las mesas y el cocinero en el canvas
def dibujar_mesas():
    canvas.delete("all")
    for mesa in mesas:
        color = "green" if mesa["estado"] == "disponible" else "red"
        canvas.create_rectangle(
            mesa["x"], mesa["y"], mesa["x"] + 50, mesa["y"] + 50, fill=color
        )
        canvas.create_text(
            mesa["x"] + 25, mesa["y"] + 25, text=f"{mesa['cliente_id'] or ''}"
        )
    # Dibujar al cocinero
    canvas.create_rectangle(
        cocinero_x, cocinero_y, cocinero_x + 50, cocinero_y + 50, fill="orange"
    )
    canvas.create_text(
        cocinero_x + 25, cocinero_y + 25, text="Cocinero", font=("Arial", 8)
    )

# Clase Cliente
class Cliente:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente
        self.tiempo_llegada = time.time()

# Clase Mesero
class Mesero(threading.Thread):
    def __init__(self, id_mesero):
        super().__init__()
        self.id_mesero = id_mesero
        self.x = 50  # Posición inicial del mesero
        self.y = 450
        self.icon = canvas.create_oval(self.x, self.y, self.x + 20, self.y + 20, fill="blue")

    def mover_hacia(self, destino_x, destino_y):
        while self.x != destino_x or self.y != destino_y:
            if self.x < destino_x:
                self.x += 3  # Aumentar velocidad del movimiento
            elif self.x > destino_x:
                self.x -= 3
            if self.y < destino_y:
                self.y += 3
            elif self.y > destino_y:
                self.y -= 3
            canvas.coords(self.icon, self.x, self.y, self.x + 20, self.y + 20)
            time.sleep(0.005)  # Reducir el tiempo de espera para mayor velocidad

    def run(self):
        global clientes_atendidos, tiempo_total_espera
        while True:
            if not clientes_en_espera.empty():
                cliente = clientes_en_espera.get()
                tiempo_espera = time.time() - cliente.tiempo_llegada
                with lock:
                    clientes_atendidos += 1
                    tiempo_total_espera += tiempo_espera
                print(f"Mesero {self.id_mesero} atendió al cliente {cliente.id_cliente} (esperó {tiempo_espera:.2f} segundos)")

                # Buscar una mesa disponible
                for mesa in mesas:
                    if mesa["estado"] == "disponible":
                        mesa["estado"] = "ocupada"
                        mesa["cliente_id"] = cliente.id_cliente
                        # Mover el mesero hacia la mesa
                        self.mover_hacia(mesa["x"] + 25, mesa["y"] + 25)
                        break

                # Enviar pedido al cocinero
                self.mover_hacia(cocinero_x + 25, cocinero_y + 25)
                print(f"Mesero {self.id_mesero} entregó el pedido del cliente {cliente.id_cliente} al cocinero.")
                pedidos_en_preparacion.put(cliente.id_cliente)

                # Esperar a que el cocinero termine
                while cliente.id_cliente not in mesas_ocupadas:
                    time.sleep(0.1)

                # Llevar el pedido de regreso a la mesa
                self.mover_hacia(mesa["x"] + 25, mesa["y"] + 25)
                print(f"Mesero {self.id_mesero} entregó el pedido del cliente {cliente.id_cliente} a la mesa.")

                # Simular tiempo para que el cliente termine de comer
                time.sleep(random.uniform(3, 5))
                with lock:
                    mesa["estado"] = "disponible"
                    mesa["cliente_id"] = None
                print(f"Cliente {cliente.id_cliente} terminó y dejó la mesa.")
                dibujar_mesas()

                # Mover el mesero de regreso a su posición inicial
                self.mover_hacia(50, 450)

# Clase Cocinero
class Cocinero(threading.Thread):
    def __init__(self, id_cocinero):
        super().__init__()
        self.id_cocinero = id_cocinero

    def run(self):
        while True:
            if not pedidos_en_preparacion.empty():
                pedido = pedidos_en_preparacion.get()
                print(f"Cocinero {self.id_cocinero} está preparando el pedido del cliente {pedido}...")
                time.sleep(random.uniform(2, 4))  # Reducir tiempo de preparación
                print(f"Cocinero {self.id_cocinero} terminó de preparar el pedido del cliente {pedido}.")
                with lock:
                    mesas_ocupadas.append(pedido)

# Función para simular la llegada de clientes
def llegada_clientes():
    cliente_id = 1
    while True:
        if mesas_disponibles > 0:
            mesas_disponibles -= 1
            cliente = Cliente(cliente_id)
            clientes_en_espera.put(cliente)
            print(f"Cliente {cliente_id} llegó al restaurante y está esperando.")
            cliente_id += 1
        else:
            print("No hay mesas disponibles. Cliente esperando afuera.")
        time.sleep(random.uniform(0.5, 1.5))  # Reducir tiempo entre llegadas

# Función para iniciar la simulación
def iniciar_simulacion():
    print("Simulación iniciada")
    threading.Thread(target=llegada_clientes, daemon=True).start()
    for i in range(2):  # Dos meseros
        Mesero(i + 1).start()
    for i in range(1):  # Un cocinero
        Cocinero(i + 1).start()

# Botón para iniciar la simulación
button = tk.Button(root, text="Iniciar Simulación", command=iniciar_simulacion)
button.pack()

# Inicia el bucle principal de la interfaz gráfica
dibujar_mesas()
root.mainloop()

