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
pedidos_en_preparacion = Queue()  # Cola para los pedidos que los cocineros prepararán
mesas_disponibles = 5
mesas_ocupadas = []  # Lista para rastrear las mesas ocupadas
lock = threading.Lock()

# Etiqueta de bienvenida
label = tk.Label(root, text="Bienvenido a la Simulación de Hilos", font=("Arial", 16))
label.pack(pady=20)

# Botón para iniciar la simulación
button = tk.Button(root, text="Iniciar Simulación")
button.pack(pady=10)

# Crear un canvas para dibujar
canvas = tk.Canvas(root, width=800, height=500, bg="white")
canvas.pack_forget()  # Ocultar el canvas inicialmente

# Clases
class Cliente:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente
        self.tiempo_llegada = time.time()

class Mesero(threading.Thread):
    def __init__(self, id_mesero):
        super().__init__()
        self.id_mesero = id_mesero

    def run(self):
        global clientes_atendidos, tiempo_total_espera
        while True:
            if not clientes_en_espera.empty():
                cliente = clientes_en_espera.get()
                tiempo_espera = time.time() - cliente.tiempo_llegada
                with lock:
                    clientes_atendidos += 1
                    tiempo_total_espera += tiempo_espera
                    mesas_ocupadas.append(cliente.id_cliente)  # Registrar cliente en mesa ocupada
                print(f"Mesero {self.id_mesero} atendió al cliente {cliente.id_cliente} (esperó {tiempo_espera:.2f} segundos)")
                
                # Enviar pedido a la cola de pedidos
                pedidos_en_preparacion.put(f"Pedido del cliente {cliente.id_cliente}")
                print(f"Mesero {self.id_mesero} envió el pedido del cliente {cliente.id_cliente} a la cocina.")
                
                time.sleep(random.randint(2, 5))  # Simular tiempo de atención

class Cocinero(threading.Thread):
    def __init__(self, id_cocinero):
        super().__init__()
        self.id_cocinero = id_cocinero

    def run(self):
        while True:
            if not pedidos_en_preparacion.empty():
                pedido = pedidos_en_preparacion.get()
                print(f"Cocinero {self.id_cocinero} está preparando {pedido}...")
                time.sleep(random.randint(3, 6))  # Simular tiempo de preparación
                print(f"Cocinero {self.id_cocinero} terminó de preparar {pedido}.")
            else:
                time.sleep(1)  # Esperar un momento antes de revisar nuevamente

# Función para simular la llegada de clientes
def llegada_clientes():
    global mesas_disponibles
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
        time.sleep(random.randint(1, 3))  # Simular tiempo entre llegadas

# Función para liberar mesas después de un tiempo aleatorio
def liberar_mesas():
    global mesas_disponibles
    while True:
        if mesas_ocupadas:
            with lock:
                cliente_id = mesas_ocupadas.pop(0)  # Liberar la primera mesa ocupada
                mesas_disponibles += 1
            print(f"Cliente {cliente_id} terminó y dejó la mesa. Mesas disponibles: {mesas_disponibles}")
        time.sleep(random.randint(5, 10))  # Tiempo aleatorio para liberar mesas

# Función para iniciar la simulación
def iniciar_simulacion():
    print("Simulación iniciada")
    label.pack_forget()
    button.pack_forget()
    canvas.pack(fill=tk.BOTH, expand=True)

    # Iniciar hilos
    threading.Thread(target=llegada_clientes, daemon=True).start()
    threading.Thread(target=liberar_mesas, daemon=True).start()
    for i in range(2):  # Dos meseros
        Mesero(i + 1).start()
    for i in range(1):  # Un cocinero
        Cocinero(i + 1).start()

    # Mostrar estadísticas en la interfaz
    actualizar_estadisticas()

# Función para actualizar estadísticas en la interfaz
def actualizar_estadisticas():
    canvas.delete("all")
    canvas.create_text(400, 50, text=f"Clientes atendidos: {clientes_atendidos}", font=("Arial", 16))
    if clientes_atendidos > 0:
        promedio_espera = tiempo_total_espera / clientes_atendidos
        canvas.create_text(400, 100, text=f"Tiempo promedio de espera: {promedio_espera:.2f} segundos", font=("Arial", 16))
    canvas.create_text(400, 150, text=f"Mesas disponibles: {mesas_disponibles}", font=("Arial", 16))
    root.after(1000, actualizar_estadisticas)  # Actualizar cada segundo

# Actualizar el comando del botón inicial
button.config(command=iniciar_simulacion)

# Inicia el bucle principal de la interfaz gráfica
root.mainloop()

