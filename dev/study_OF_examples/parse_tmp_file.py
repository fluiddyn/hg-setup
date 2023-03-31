#!/usr/bin/env python3

import sys
from pathlib import Path

from fluidsimfoam.foam_input_files import dump, parse

if len(sys.argv) == 2:
    path = Path(sys.argv[-1])
else:
    path = Path("tmp_file")

assert path.exists()

tree = parse(path.read_text())

dumped = dump(tree)
assert tree == parse(dumped)
