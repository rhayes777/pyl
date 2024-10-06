import inspect
from pathlib import Path
from typing import List


class Module:
    def __init__(
        self,
        path: Path,
        functions: List["Function"] = None,
    ):
        self.path = path
        self.functions = functions or []

    @property
    def target_path(self):
        return self.path.with_stem(f"{self.path.stem}_pylm.py")


class Function:
    def __init__(self, function, module: Module):
        self.function = function
        self.module = module

    @property
    def name(self):
        return self.function.__name__

    @property
    def signature(self):
        return str(inspect.signature(self.function))

    @property
    def docs(self):
        return self.function.__doc__

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class Session:
    def __init__(self):
        self.modules_by_path = {}

    def jit(self, function):
        module_path = Path(function.__code__.co_filename)

        if module_path not in self.modules_by_path:
            self.modules_by_path[module_path] = Module(module_path)

        module = self.modules_by_path[module_path]
        function_ = Function(function, module)
        module.functions.append(function_)

        return function_

    @property
    def modules(self):
        return self.modules_by_path.keys()

    @property
    def functions(self):
        return [
            function
            for functions in self.modules_by_path.values()
            for function in functions
        ]
