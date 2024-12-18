from shutil import rmtree
from pathlib import Path

p = Path(r'C:\Program Files\Mercurial')
if p.exists():
    rmtree(p)
