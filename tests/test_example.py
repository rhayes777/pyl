from pathlib import Path

from pylm.module import Module


def test_register_function():
    example_path = Path(__file__).parents[1] / "pylm/example.pylm"
    module = Module(example_path)
    function = module.functions[0]
    assert function.docs == "\n    Add together two numbers\n    "
    assert function.signature == "(a, b)"
    assert function.name == "function"
