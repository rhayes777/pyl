from pathlib import Path

from pylm.module import Module


def test_register_function():
    example_path = Path(__file__).parent / "example.pylm"
    module = Module(example_path)
    function = module.functions[0]
    assert function.docs == '\n    Add together two numbers\n    '
