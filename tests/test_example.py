from pathlib import Path

from pylm.compiler import Compiler


def test_register_function():
    example_path = Path(__file__).parent / "example.pylm"
    compiler = Compiler(example_path)
    assert len(compiler.functions) > 0
