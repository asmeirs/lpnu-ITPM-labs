class CalculatorController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.buttons['+'].config(command=self.handle_add)
        self.view.buttons['-'].config(command=self.handle_subtract)
        self.view.buttons['*'].config(command=self.handle_multiply)
        self.view.buttons['/'].config(command=self.handle_divide)

    def handle_add(self):
        self._calculate(self.model.add)

    def handle_subtract(self):
        self._calculate(self.model.subtract)

    def handle_multiply(self):
        self._calculate(self.model.multiply)

    def handle_divide(self):
        self._calculate(self.model.divide)

    def _calculate(self, operation):
        a, b = self.view.get_input()
        if a is None or b is None:
            self.view.set_result("Invalid input")
            return
        result = operation(a, b)
        self.view.set_result(result)
