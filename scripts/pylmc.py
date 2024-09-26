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

module = Module(args.source)

compiler = Compiler(module)

with open(source_path.with_suffix(".py"), "w") as f:
    f.write(compiler.compiled_module())
