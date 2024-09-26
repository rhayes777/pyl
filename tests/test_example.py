import shutil
from pathlib import Path
import pytest

from pylm.module import Module
from pylm.module_updater import ModuleUpdater


@pytest.fixture
def example_path():
    return Path(__file__).parents[1] / "pylm/example.pylm"


def test_register_function(example_path):
    module = Module(example_path)
    function = module.functions[0]
    assert function.docs == "\n    Add together two numbers\n    "
    assert function.signature == "(a, b)"
    assert function.name == "function"


@pytest.fixture
def example_target(example_path):
    target = Path(__file__).parent / "example.py"
    shutil.copy(example_path, target)
    yield target
    target.unlink()


def test_module_updater(example_target):
    updater = ModuleUpdater(example_target)
    updater["function"].update("def function():\n    pass")
    updater.commit()

    assert (
        """
def function():
    pass
"""
        in example_target.read_text()
    )
