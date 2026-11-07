#!/usr/bin/env python3
"""Transactional manual installer for both skins and their own Python modules."""
import os
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime


def install(source, destination):
    source=Path(source);destination=Path(destination)
    share=destination/'usr/share/enigma2'
    python=destination/'usr/lib/enigma2/python'
    units=[(source/'Polsq',share/'Polsq'),(source/'PolsqLarge',share/'PolsqLarge'),
           (source/'runtime/Plugins/Extensions/PolsqSettings',python/'Plugins/Extensions/PolsqSettings'),
           (source/'runtime/Components/Converter/PolsqEventRemaining.py',python/'Components/Converter/PolsqEventRemaining.py'),
           (source/'runtime/Components/Renderer/PolsqSummary.py',python/'Components/Renderer/PolsqSummary.py')]
    for src,target in units:
        if not src.exists():raise RuntimeError('Niekompletna paczka: '+str(src))
        if target.is_symlink():raise RuntimeError('Katalog docelowy jest dowiązaniem: '+str(target))
    staged=[];committed=[];backups=[]
    stamp=datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+str(os.getpid())
    try:
        for src,target in units:
            target.parent.mkdir(parents=True,exist_ok=True)
            staging=Path(tempfile.mkdtemp(prefix='.Polsq-stage-',dir=target.parent))
            item=staging/target.name
            staged.append(staging)
            if src.is_dir():shutil.copytree(src,item)
            else:shutil.copyfile(src,item)
            for path in [item]+(list(item.rglob('*')) if item.is_dir() else []):
                path.chmod(0o755 if path.is_dir() else 0o644)
        for (src,target),staging in zip(units,staged):
            backup=None
            if target.exists():
                if target.name=='Polsq':backup=target.with_name('Polsq.backup-'+stamp)
                else:
                    backup=share/'.Polsq-backups'/stamp/target.name
                    backup.parent.mkdir(parents=True,exist_ok=True)
                target.rename(backup);backups.append(backup)
            committed.append((target,backup))
            (staging/target.name).rename(target)
    except BaseException:
        for target,backup in reversed(committed):
            if target.exists():
                if target.is_dir():shutil.rmtree(target)
                else:target.unlink()
            if backup is not None and backup.exists():backup.rename(target)
        raise
    finally:
        for staging in staged:shutil.rmtree(staging,ignore_errors=True)
    for backup in backups:print('Kopia poprzedniej wersji: '+str(backup))
    return share/'Polsq'


def main():
    source=Path(sys.argv[1]);prefix=os.environ.get('DESTDIR','')
    if not prefix and not Path('/usr/share/enigma2').is_dir():
        raise RuntimeError('To nie wygląda na dekoder Enigma2: brak /usr/share/enigma2.')
    print('Polsq: instalowanie plików skórki...')
    target=install(source,Path(prefix or '/'))
    print('\nPolsq — INSTALACJA ZAKOŃCZONA POMYŚLNIE')
    print('Wersja: '+(target/'VERSION').read_text().strip())
    print('Wtyczki → Polsq — wygląd: wybierz Standard lub Duże napisy i zapisz.')
    print('Uruchom ponownie interfejs GUI, aby wczytać zmiany.')


if __name__=='__main__':
    try:main()
    except Exception as error:
        print('Polsq: instalacja przerwana — '+str(error),file=sys.stderr)
        sys.exit(1)
