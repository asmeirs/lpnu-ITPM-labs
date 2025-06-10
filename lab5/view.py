import tkinter as tk

class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("MVC Calculator")

        self.entry1 = tk.Entry(root)
        self.entry2 = tk.Entry(root)
        self.entry1.pack()
        self.entry2.pack()

        self.result_label = tk.Label(root, text="Result: ")
        self.result_label.pack()

        self.buttons = {}
        for op in ['+', '-', '*', '/']:
            btn = tk.Button(root, text=op)
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons[op] = btn

    def get_input(self):
        try:
            return float(self.entry1.get()), float(self.entry2.get())
        except ValueError:
            return None, None

    def set_result(self, result):
        self.result_label.config(text=f"Result: {result}")
