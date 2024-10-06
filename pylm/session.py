import inspect
from collections import defaultdict
from pathlib import Path
from typing import List


class Module:
    def __init__(
        self,
        path: Path,
        functions: List["Function"],
    ):
        self.path = path
        self.functions = functions


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

    @property
    def modules(self):
        functions_by_module = defaultdict(list)
        for function in self.functions:
            module_path = Path(function.function.__code__.co_filename)
            functions_by_module[module_path].append(function)

        return [
            Module(module_path, functions)
            for module_path, functions in functions_by_module.items()
        ]
