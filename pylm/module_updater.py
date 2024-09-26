import ast
from pathlib import Path


class ModuleUpdater:
    def __init__(self, path: Path):
        self.path = path
        self.ast = ast.parse(self.path.read_text())

    def __getitem__(self, name: str):
        for i, item in enumerate(self.ast.body):
            try:
                if getattr(item, "name") == name:
                    return Item(self, i)
            except AttributeError:
                pass
        raise KeyError(f"No item found with name {name}")

    def commit(self):
        with open(self.path, "w") as f:
            f.write(ast.unparse(self.ast))


class Item:
    def __init__(
        self,
        updater: ModuleUpdater,
        index: int,
    ):
        self.updater = updater
        self.index = index

    def update(self, code: str):
        self.updater.ast.body[self.index] = ast.parse(code)
