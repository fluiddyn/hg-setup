import os

from pathlib import Path
from pprint import pprint
from shutil import which

pprint(os.environ["PATH"])

hg = Path(which("hg"))
print(hg)
print(hg.read_text(encoding="utf-8"))
print(sorted(hg.parent.glob("*")))
