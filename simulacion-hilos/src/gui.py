from tkinter import Tk, Canvas
import time
import threading

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulación de Hilos del Procesador")
        self.canvas = Canvas(master, width=800, height=600, bg='white')
        self.canvas.pack()
        self.icon_id = self.canvas.create_oval(390, 290, 410, 310, fill='blue')  # Crea un círculo en lugar de una imagen
        self.is_running = False

    def start_animation(self):
        self.is_running = True
        self.animate()

    def stop_animation(self):
        self.is_running = False

    def animate(self):
        if self.is_running:
            self.canvas.move(self.icon_id, 5, 0)  # Mueve el círculo a la derecha
            self.master.update()
            self.master.after(100, self.animate)  # Llama a animate cada 100 ms

    def update_status(self, message):
        self.canvas.create_text(400, 550, text=message, font=('Helvetica', 12))

def main():
    root = Tk()
    gui = GUI(root)
    gui.start_animation()
    root.mainloop()

if __name__ == "__main__":
    main()