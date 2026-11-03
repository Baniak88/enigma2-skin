#!/usr/bin/env python3
"""Wizualizuje prawdziwe współrzędne XML, z przykładowymi danymi."""
from html import escape
from pathlib import Path
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKIN = ET.parse(ROOT / 'CanalPL/skin.xml').getroot()
COLORS = {c.get('name'): c.get('value')[-6:] for c in SKIN.findall('colors/color')}


def color(name):
    return '#' + COLORS.get(name, 'f5f5f5')


def rect(x, y, w, h, fill):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'


def text(x, y, w, h, value, size=30, fill='#f5f5f5', align='left', nowrap=False):
    anchor = 'end' if align == 'right' else 'middle' if align == 'center' else 'start'
    tx = x + w if anchor == 'end' else x + w / 2 if anchor == 'middle' else x
    lines = []
    for paragraph in value.replace('\\n', '\n').splitlines():
        if nowrap:
            capacity = max(1, int(w / (size * .56)))
            lines.append(paragraph if len(paragraph) <= capacity else paragraph[:capacity - 1] + '…')
        else:
            lines.extend(textwrap.wrap(paragraph, max(1, int(w / (size * .56)))))
    lines = lines[:max(1, int(h / (size * 1.25)))]
    return ''.join(f'<text x="{tx}" y="{y + size + i * size * 1.25}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{escape(line)}</text>' for i, line in enumerate(lines))


def sample(node):
    source = node.get('source', '')
    converter = node.find('convert')
    kind = converter.get('type') if converter is not None else ''
    value = converter.text if converter is not None else ''
    if source == 'global.CurrentTime':
        return '20:45'
    if source == 'title':
        return 'Menu główne'
    if 'key_' in source or 'key_' in node.get('name', ''):
        key = (source or node.get('name')).split('_')[-1]
        return {'red': 'Wszystkie', 'green': 'Satelity', 'yellow': 'Dostawcy', 'blue': 'Ulubione'}.get(key, '')
    if source == 'session.RecordState':
        return ''  # Nagrywanie wyłączone w przykładzie.
    if kind == 'ServiceName':
        return 'CANAL+ PREMIUM'
    if kind == 'EventTime':
        if value == 'Remaining':
            return '+45 min'
        return '21:30' if source.endswith('Next') else ('– 21:30' if value == 'EndTime' else '20:00')
    if kind == 'EventName':
        if value == 'ExtendedDescription':
            return 'Wieczór z wielkim kinem. Nieoczekiwane spotkanie zmienia życie bohaterów. Opowieść o odwadze, przyjaźni i wyborach, które zostają z nami na długo.'
        return 'Nocna zmiana' if source.endswith('Next') else 'Wszystko przed nami'
    return node.get('text', '')


def render(name, target):
    screen = next(s for s in SKIN.findall('screen') if s.get('name') == name)
    ox, oy = map(int, screen.get('position').split(','))
    sw, sh = map(int, screen.get('size').split(','))
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">',
           f'<title>CanalPL — {name} — wizualizacja, dane przykładowe</title>',
           '<g font-family="DejaVu Sans, sans-serif">',
           rect(0, 0, 1920, 1080, '#20282c')]
    if name == 'InfoBar':
        out.append(text(72, 400, 1776, 180, 'Miejsce na obraz telewizyjny', 42, '#758187', 'center'))
    out.append(rect(ox, oy, sw, sh, color(screen.get('backgroundColor'))))
    for node in screen:
        x, y = map(int, node.get('position').split(','))
        w, h = map(int, node.get('size').split(','))
        x, y = x + ox, y + oy
        bg = node.get('backgroundColor')
        if bg and node.get('transparent') != '1':
            out.append(rect(x, y, w, h, color(bg)))
        if node.get('render') == 'Progress':
            out.append(rect(x, y, w, h, color('cpLine')))
            out.append(rect(x, y, int(w * .5), h, color('cpGreen')))
        elif node.get('source') == 'menu' or node.get('name') == 'list':
            menu = node.get('source') == 'menu'
            rows = ['Telewizja', 'Program TV', 'Nagrania', 'Wtyczki', 'Ustawienia', 'Czuwanie / restart'] if menu else [f'{i + 1:02d}   {s}' for i, s in enumerate(['CANAL+ PREMIUM', 'CANAL+ FILM', 'CANAL+ SPORT', 'CANAL+ SERIALE', 'TVP 1 HD', 'TVP 2 HD', 'TVN HD', 'Polsat HD', 'TVN 24', 'Ale kino+'])]
            rh = 72 if menu else 70
            for i, row in enumerate(rows):
                if i == 0:
                    out.append(rect(x, y + i * rh, w, rh, color('cpGreen')))
                out.append(text(x + 24, y + i * rh + 12, w - 48, rh - 12, row, 34 if menu else 30, color('cpBackground' if i == 0 else 'cpWhite'), nowrap=True))
        else:
            size = int(node.get('font', 'Regular;30').split(';')[-1])
            out.append(text(x, y, w, h, sample(node), size, color(node.get('foregroundColor', 'cpWhite')), node.get('halign', 'left'), node.get('noWrap') == '1'))
    out.extend(['</g>', '</svg>'])
    path = ROOT / 'docs' / target
    path.parent.mkdir(exist_ok=True)
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(path)


if __name__ == '__main__':
    for name, target in [('InfoBar', 'infobar.svg'), ('ChannelSelection', 'channels.svg'), ('Menu', 'menu.svg')]:
        render(name, target)
