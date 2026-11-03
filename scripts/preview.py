#!/usr/bin/env python3
"""Podglądy prawdziwych współrzędnych XML z danymi przykładowymi, bez emulacji GUI."""
import argparse
import base64
from html import escape
import io
from pathlib import Path
import textwrap
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]
SKIN=E.parse(ROOT/'CanalPL/skin.xml').getroot()
COLORS={c.get('name'):'#'+c.get('value')[-6:] for c in SKIN.findall('colors/color')}
CHANNELS=['CANAL+ PREMIUM','CANAL+ FILM','CANAL+ SPORT','CANAL+ SERIALE','TVP 1 HD','TVP 2 HD','TVN HD','Polsat HD']
SHORT=['C+ PREMIUM','C+ FILM','C+ SPORT','C+ SERIALE','TVP 1','TVP 2','TVN','POLSAT']
SHOWS=['Wszystko przed nami','Wieczór filmowy','Magazyn sportowy','Nowy rozdział','Wiadomości dnia','Na dobre i na złe','Fakty','Wydarzenia']
out=[]


def color(value):
    return COLORS.get(value,value if value and value.startswith('#') else COLORS['white'])


def rect(x,y,w,h,fill):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color(fill)}"/>')


def text(x,y,w,h,value,size=28,fill='white',align='left',nowrap=False):
    lines=[]
    for paragraph in value.replace('\\n','\n').splitlines():
        capacity=max(1,int(w/(size*.57)))
        lines.extend([paragraph[:capacity-1]+'…' if len(paragraph)>capacity else paragraph] if nowrap else textwrap.wrap(paragraph,capacity))
        if not paragraph:lines.append('')
    anchor={'left':'start','center':'middle','right':'end'}.get(align,'start')
    tx=x+w if anchor=='end' else x+w/2 if anchor=='middle' else x
    for i,line in enumerate(lines[:max(1,int(h/(size*1.25)))]):
        out.append(f'<text x="{tx}" y="{y+size+i*size*1.25}" font-size="{size}" fill="{color(fill)}" text-anchor="{anchor}">{escape(line)}</text>')


def png(path,x,y,w,h):
    encoded=base64.b64encode(path.read_bytes()).decode()
    out.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{encoded}"/>')


def fake_picon(index,x,y,w,h):
    # Celowo tekstowa próbka, bez kopiowania prawdziwych logo.
    rect(x,y,w,h,'panel');rect(x,y,w,4,'green')
    text(x+4,y+h*.25,w-8,h*.7,SHORT[index],max(15,min(30,int(w/8))),'white','center')


def value(node,screen):
    src=node.get('source','');key=node.get('name','');conv=node.find('convert')
    kind=conv.get('type') if conv is not None else '';arg=conv.text if conv is not None else ''
    if src=='Title':return {'Menu':'Menu główne','ChannelSelection':'Ulubione — telewizja','BouquetSelector':'Wybierz bukiet','GraphicalEPG':'Ulubione — wtorek, 3 listopada','Setup':'Ustawienia interfejsu'}.get(screen,'')
    if src=='global.CurrentTime':return '20:45'
    if src=='description':return 'Informacje o dekoderze, obrazie OpenATV, tunerach, pamięci i połączeniu sieciowym.'
    key=src or key
    if key.startswith('key_'):
        if screen=='ChannelSelection':return {'key_red':'Wszystkie','key_green':'Listy odbioru','key_yellow':'Dostawcy','key_blue':'Bukiety'}.get(key,'')
        if screen=='BouquetSelector':return {'key_red':'Anuluj','key_green':'Wybierz'}.get(key,'')
        if screen=='Menu':return {'key_red':'Wyjdź','key_blue':'Tryb edycji'}.get(key,'')
        return {'key_red':'Wyszukaj','key_green':'Dodaj timer','key_yellow':'Szukaj w EPG','key_blue':'AutoTimer'}.get(key,'')
    if src=='session.RecordState':return ''
    if kind=='ServiceName':return CHANNELS[0]
    if kind=='EventName':
        if arg=='ExtendedDescription':return 'Wieczór z wielkim kinem. Nieoczekiwane spotkanie zmienia życie bohaterów. Opowieść o odwadze, przyjaźni i wyborach, które zostają z nami na długo.'
        return 'Nocna zmiana' if src.endswith('Next') else SHOWS[0]
    if kind=='EventTime':
        return '+45 min' if arg=='Remaining' else '21:30' if src.endswith('Next') else '– 21:30' if arg=='EndTime' else '20:00'
    return node.get('text','')


def draw_list(name,key,x,y,w,h):
    if name=='Menu':
        rows=['Informacje','Timery','Nagrania','Wtyczki','Ustawienia','Czuwanie / restart']
        icons=['information','timermenu','movie_selection','plugin_selection','setup','shutdown']
        for i,row in enumerate(rows):
            if i==0:rect(x,y,w,80,'green')
            png(ROOT/'CanalPL/mainmenu'/(icons[i]+'.png'),x+16,y+i*80+12,56,56)
            text(x+92,y+i*80+18,w-116,60,row,32,'bg' if i==0 else 'white',nowrap=True)
    elif name=='BouquetSelector':
        for i,row in enumerate(['Ulubione','CANAL+','Filmy i seriale','Sport','Informacyjne','Dzieci','Dokumentalne','Radio']):
            if i==0:rect(x,y,w,80,'green')
            text(x+24,y+i*80+18,w-48,60,row,32,'bg' if i==0 else 'white',nowrap=True)
    elif name=='ChannelSelection':
        for i,(channel,show) in enumerate(zip(CHANNELS,SHOWS)):
            rh=76
            if i==0:rect(x,y,w,rh,'green')
            text(x+10,y+i*rh+22,70,50,str(i+1),25,'bg' if i==0 else 'muted','right')
            fake_picon(i,x+100,y+i*rh+8,100,60)
            text(x+224,y+i*rh+6,w-250,38,channel,28,'bg' if i==0 else 'white',nowrap=True)
            text(x+224,y+i*rh+44,w-250,30,show,23,'bg' if i==0 else 'muted',nowrap=True)
    elif name=='GraphicalEPG' and key=='list':
        service=320;rowh=h/8;area=w-service
        for i,(channel,show) in enumerate(zip(CHANNELS,SHOWS)):
            yy=y+i*rowh
            rect(x,yy,service-2,rowh-2,'panel')
            fake_picon(i,x+12,yy+8,80,rowh-16)
            text(x+106,yy+18,service-118,rowh-18,channel,23,'green' if i==0 else 'white',nowrap=True)
            titles=[show,'Nocna zmiana' if i==0 else 'Kolejna audycja','Program wieczorny']
            for j,show in enumerate(titles):
                xx=x+service+j*area/3
                rect(xx,yy,area/3-2,rowh-2,'green' if i==0 and j==0 else 'panel')
                text(xx+12,yy+18,area/3-26,rowh-18,show,25,'bg' if i==0 and j==0 else 'white',nowrap=True)


def render(name,target,make_png=False):
    global out
    s=SKIN.find(f"screen[@name='{name}']");ox,oy=map(int,s.get('position').split(','));sw,sh=map(int,s.get('size').split(','))
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">',f'<title>CanalPL — {name} — dane przykładowe</title>','<g font-family="DejaVu Sans, sans-serif">']
    rect(0,0,1920,1080,'#20282c')
    if name=='InfoBar':text(64,350,1792,140,'Miejsce na obraz telewizyjny',42,'#758187','center')
    rect(ox,oy,sw,sh,s.get('backgroundColor'))
    for n in s:
        x,y=map(int,n.get('position').split(','));w,h=map(int,n.get('size').split(','));x+=ox;y+=oy
        key=n.get('name') or n.get('source','')
        if key in ('lab1','number','bouquetlist') or re_timeline(key):continue
        if n.get('backgroundColor') and n.get('transparent')!='1':rect(x,y,w,h,n.get('backgroundColor'))
        if n.get('render')=='Picon':fake_picon(0,x,y,w,h)
        elif n.tag=='ePixmap':png(ROOT/n.get('pixmap'),x,y,w,h)
        elif key=='menuimage':png(ROOT/'CanalPL/mainmenu/information.png',x,y,w,h)
        elif key=='timeline_text':
            for i,t in enumerate(['20:00','20:30','21:00','21:30','22:00','22:30']):text(x+320+i*(w-320)/6,y,(w-320)/6,h,t,26,'muted')
        elif n.get('render')=='Progress':rect(x,y,w,h,'line');rect(x,y,int(w*.5),h,'green')
        elif key in ('menu','list'):
            draw_list(name,key,x,y,w,h)
        else:
            size=int(n.get('font','Regular;28').split(';')[-1])
            text(x,y,w,h,value(n,name),size,n.get('foregroundColor','white'),n.get('halign','left'),n.get('noWrap')=='1')
    if name=='GraphicalEPG':rect(64+320+360,366,3,560,'green')
    out+=['</g>','</svg>']
    dest=ROOT/'docs'/target;dest.parent.mkdir(exist_ok=True);dest.write_text('\n'.join(out)+'\n')
    if make_png:render_png(dest)
    print(dest)


def re_timeline(key):
    return key.startswith('timeline') and key!='timeline_text'


def render_png(path):
    from PIL import Image,ImageDraw,ImageFont
    im=Image.new('RGB',(1920,1080));draw=ImageDraw.Draw(im)
    for n in E.parse(path).getroot().iter():
        tag=n.tag.split('}')[-1]
        if tag=='rect':
            x,y,w,h=[float(n.get(k)) for k in ('x','y','width','height')];draw.rectangle((x,y,x+w,y+h),fill=n.get('fill'))
        elif tag=='text':
            font=ImageFont.truetype('DejaVuSans.ttf',int(n.get('font-size')))
            draw.text((float(n.get('x')),float(n.get('y'))),n.text or '',font=font,fill=n.get('fill'),anchor={'start':'ls','middle':'ms','end':'rs'}[n.get('text-anchor')])
        elif tag=='image':
            pic=Image.open(io.BytesIO(base64.b64decode(n.get('href').split(',')[1]))).convert('RGBA')
            pic=pic.resize((int(float(n.get('width'))),int(float(n.get('height')))))
            im.paste(pic,(int(float(n.get('x'))),int(float(n.get('y')))),pic)
    im.resize((1280,720),Image.Resampling.LANCZOS).save(path.with_suffix('.png'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--png',action='store_true');args=p.parse_args()
    for name,target in [('Menu','menu.svg'),('ChannelSelection','channels.svg'),('BouquetSelector','bouquets.svg'),('GraphicalEPG','epg.svg'),('InfoBar','infobar.svg')]:
        render(name,target,args.png)
