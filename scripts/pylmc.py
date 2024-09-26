#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path

from pylm.compiler import Compiler
from pylm.module import Module

argument_parser = ArgumentParser()

argument_parser.add_argument(
    "source",
    type=Path,
)

args = argument_parser.parse_args()

source_path = args.source


def compile_module(path: Path):
    module = Module(path)
    compiler = Compiler(module)
    compiler.run()
    with open(path.with_suffix(".py"), "w") as f:
        f.write(compiler.compiled_module())


if source_path.is_dir():
    for module_path in source_path.rglob("*.pylm"):
        compile_module(module_path)
    exit()

compile_module(source_path)
