import inspect


class Function:
    def __init__(self, function):
        self.function = function

    @property
    def name(self):
        return self.function.__name__

    @property
    def signature(self):
        return str(inspect.signature(self.function))

    @property
    def docs(self):
        return self.function.__doc__


class Session:
    def __init__(self):
        self.functions = []

    def jit(self, function):
        self.functions.append(Function(function))

