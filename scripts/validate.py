#!/usr/bin/env python3
"""Kontrole statyczne. Nie zastępują uruchomienia Enigma2 na dekoderze."""
import ast
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def validate():
    skin = ET.parse(ROOT / 'CanalPL/skin.xml').getroot()
    assert skin.tag == 'skin'
    res = skin.find('output/resolution')
    assert (res.get('xres'), res.get('yres')) == ('1920', '1080')
    colors = {c.get('name'): c.get('value') for c in skin.findall('colors/color')}
    assert all(re.fullmatch(r'#[0-9a-fA-F]{8}', c) for c in colors.values())
    names = [s.get('name') for s in skin.findall('screen')]
    assert len(names) == len(set(names)), 'Powtórzona nazwa ekranu'
    for screen in skin.findall('screen'):
        sw, sh = map(int, screen.get('size').split(','))
        sx, sy = map(int, screen.get('position').split(','))
        assert 0 <= sx and 0 <= sy and sx + sw <= 1920 and sy + sh <= 1080
        for node in screen:
            x, y = map(int, node.get('position').split(','))
            w, h = map(int, node.get('size').split(','))
            assert min(x, y) >= 0 and min(w, h) > 0
            assert x + w <= sw and y + h <= sh, (screen.get('name'), node.attrib)
            if node.tag == 'widget':
                assert bool(node.get('name')) != bool(node.get('source'))
                if node.get('source'):
                    assert node.get('render')
            for key, value in node.attrib.items():
                if 'color' in key.lower():
                    assert value in colors or re.fullmatch(r'#[0-9a-fA-F]{6,8}', value)
            for convert in node.findall('convert'):
                if convert.get('type') == 'TemplatedMultiContent':
                    ast.parse(convert.text.strip(), mode='eval')
                if convert.get('type') == 'EventTime':
                    assert convert.text in {'StartTime', 'EndTime', 'Progress', 'Duration', 'Remaining'}
    # Brak zależności od własnych komponentów lub niedołączonych grafik.
    assert not skin.findall('.//ePixmap')
    assert not skin.findall('.//include')
    print(f'OK: XML, {len(names)} ekranów, kolory, granice i szablon menu.')


if __name__ == '__main__':
    validate()
