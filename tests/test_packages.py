import gzip
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import PACKAGE, VERSION, build
from validate import validate


def read_ar(data):
    assert data[:8]==b'!<arch>\n'
    result={};offset=8
    while offset<len(data):
        h=data[offset:offset+60];assert h[58:]==b'`\n'
        name=h[:16].decode().strip().rstrip('/');size=int(h[48:58])
        result[name]=data[offset+60:offset+60+size]
        offset+=60+size+size%2
    assert offset==len(data)
    return result


class Packages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build()

    def test_skin_contracts_and_assets(self):
        validate()

    def test_ipk_complete_payload(self):
        files=read_ar((ROOT/'dist'/PACKAGE).read_bytes())
        self.assertEqual(set(files),{'debian-binary','control.tar.gz','data.tar.gz'})
        self.assertEqual(files['debian-binary'],b'2.0\n')
        with tarfile.open(fileobj=io.BytesIO(files['control.tar.gz'])) as t:
            control=t.extractfile('control').read().decode()
        self.assertIn('Architecture: all\n',control)
        self.assertIn('Depends: enigma2\n',control)
        with tarfile.open(fileobj=io.BytesIO(files['data.tar.gz'])) as t:
            names=set(t.getnames())
            expected={'usr/share/enigma2/'+str(p.relative_to(ROOT)) for p in (ROOT/'CanalPL').rglob('*') if p.is_file()}
            self.assertEqual(names,expected)
            for p in (ROOT/'CanalPL').rglob('*'):
                if p.is_file():
                    name='usr/share/enigma2/'+str(p.relative_to(ROOT))
                    self.assertEqual(t.extractfile(name).read(),p.read_bytes())
                    self.assertEqual(t.getmember(name).mode,0o644)

    def test_manual_install_backup_and_symlink_refusal(self):
        with tempfile.TemporaryDirectory() as temp:
            temp=Path(temp);source=temp/'package'
            with tarfile.open(ROOT/'dist'/f'CanalPL-{VERSION}.tar.gz') as t:
                for m in t:
                    self.assertFalse(Path(m.name).is_absolute())
                    self.assertNotIn('..',Path(m.name).parts)
                t.extractall(source,filter='data')
            env=dict(os.environ,DESTDIR=str(temp/'receiver'))
            target=temp/'receiver/usr/share/enigma2/CanalPL'
            def install():
                return subprocess.run(['sh',str(source/'install.sh')],env=env,capture_output=True,text=True)
            first=install();self.assertEqual(first.returncode,0,first.stderr)
            for p in (ROOT/'CanalPL').rglob('*'):
                if p.is_file():self.assertEqual((target/p.relative_to(ROOT/'CanalPL')).read_bytes(),p.read_bytes())
            (target/'skin.xml').write_text('old skin')
            (target/'user-note').write_text('keep in backup')
            second=install();self.assertEqual(second.returncode,0,second.stderr)
            backups=list(target.parent.glob('CanalPL.backup-*'));self.assertEqual(len(backups),1)
            self.assertEqual((backups[0]/'skin.xml').read_text(),'old skin')
            self.assertEqual((backups[0]/'user-note').read_text(),'keep in backup')
            self.assertFalse((target/'user-note').exists())
            import shutil
            shutil.rmtree(target);outside=temp/'outside';outside.mkdir();target.symlink_to(outside,target_is_directory=True)
            self.assertNotEqual(install().returncode,0)
            self.assertFalse(list(outside.iterdir()))

    def test_reproducible_archives(self):
        before={p.name:p.read_bytes() for p in (ROOT/'dist').glob('*0.2.0*')}
        build()
        self.assertEqual(before,{p.name:p.read_bytes() for p in (ROOT/'dist').glob('*0.2.0*')})


if __name__=='__main__':
    unittest.main()
