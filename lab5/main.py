import tkinter as tk
from model import CalculatorModel
from view import CalculatorView
from controller import CalculatorController

if __name__ == "__main__":
    root = tk.Tk()
    model = CalculatorModel()
    view = CalculatorView(root)
    controller = CalculatorController(view, model)
    root.mainloop()
