import pytest

from pylm import example


@pytest.fixture
def session():
    return example.pylm


def test_functions(session):
    assert session.functions[0].name == "function"


def test_modules(session):
    assert len(session.modules) == 1
