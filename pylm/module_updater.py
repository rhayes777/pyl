import ast
from pathlib import Path


class ModuleUpdater:
    def __init__(self, path: Path):
        self.path = path

    def ast(self):
        return ast.parse(self.path.read_text())

    def __setitem__(self, key: str, value: str):
        new_item = ast.parse(value)
        tree = self.ast()
        tree.body = [
            item
            if not hasattr(
                item,
                "name",
            )
            or getattr(item, "name") != key
            else new_item
            for item in tree.body
        ]
        with open(self.path, "w") as f:
            f.write(ast.unparse(tree))
