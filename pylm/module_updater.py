import ast
from pathlib import Path


class ModuleUpdater:
    def __init__(self, path: Path):
        path.touch()
        self.path = path
        self.ast = ast.parse(self.path.read_text())

    def add_function(self, code: str):
        self.ast.body.append(ast.parse(code))

    def exists(self, name: str):
        for i, item in enumerate(self.ast.body):
            try:
                if getattr(item, "name") == name:
                    return True
            except AttributeError:
                pass

        return False

    def commit(self):
        with open(self.path, "w") as f:
            f.write(ast.unparse(self.ast))
