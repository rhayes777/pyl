class Session:
    def __init__(self):
        self.functions = []

    def jit(self, function):
        self.functions.append(function)

