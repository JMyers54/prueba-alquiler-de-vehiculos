from Views.interfaz import Interfaz
import tkinter as tk

class Main():
    def __init__(self) :
        self.root = tk.Tk()
        self.app = Interfaz(self.root)
        self.root.mainloop()
if __name__== "__main__":
    Main()