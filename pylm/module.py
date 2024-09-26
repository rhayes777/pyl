from functools import cached_property
from pathlib import Path


class Module:
    def __init__(self, path: Path):
        self.path = path

    @cached_property
    def code(self):
        return self.path.read_text()

    @cached_property
    def functions(self):
        exec(self.code, globals())
        session = globals().get("pylm")
        return session.functions
