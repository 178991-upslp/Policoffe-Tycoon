class Simulation:
    def __init__(self):
        self.running = False
        self.threads = []

    def start(self):
        self.running = True
        self.threads = [self.create_thread(i) for i in range(4)]  # Simulando 4 hilos

    def create_thread(self, thread_id):
        # Aquí se puede agregar la lógica para simular el trabajo de un hilo
        return f"Hilo {thread_id} en ejecución"

    def stop(self):
        self.running = False
        self.threads = []

    def update(self):
        if self.running:
            # Aquí se puede agregar la lógica para actualizar el estado de los hilos
            return [f"Hilo {i} activo" for i in range(len(self.threads))]
        return []