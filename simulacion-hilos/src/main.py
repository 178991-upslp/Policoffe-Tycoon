import tkinter as tk
from gui import GUI
from simulation import Simulation

def main():
    root = tk.Tk()
    root.title("Simulación de Hilos del Procesador")
    
    gui = GUI(root)
    simulation = Simulation(gui)

    gui.start_button.config(command=simulation.start)
    gui.stop_button.config(command=simulation.stop)

    root.mainloop()

if __name__ == "__main__":
    main()