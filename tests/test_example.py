import shutil
from pathlib import Path
import pytest

from pylm.module import Module


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
    shutil.rmtree(target)


def test_module_updater(target):
    shutil
