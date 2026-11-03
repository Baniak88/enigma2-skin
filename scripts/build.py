#!/usr/bin/env python3
"""Buduje paczkę do ręcznej instalacji; wymaga wyłącznie Python 3."""
import io
from pathlib import Path
import tarfile
from validate import validate

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1.0'


def build():
    validate()
    target = ROOT / 'dist' / f'CanalPL-{VERSION}.tar.gz'
    target.parent.mkdir(exist_ok=True)
    files = ['CanalPL/skin.xml', 'install.sh', 'README.md', 'LICENSE']
    with tarfile.open(target, 'w:gz') as archive:
        for name in files:
            data = (ROOT / name).read_bytes()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o755 if name.endswith('.sh') else 0o644
            info.mtime = 0
            archive.addfile(info, io.BytesIO(data))
    print(target)


if __name__ == '__main__':
    build()
