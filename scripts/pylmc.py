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

module = Module(args.source)

compiler = Compiler(module)

for function in compiler.compiled_functions():
    print(function.implementation)
