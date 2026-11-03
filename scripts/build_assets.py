#!/usr/bin/env python3
"""Małe autorskie PNG bez zewnętrznych bibliotek i bez logotypów operatorów."""
from pathlib import Path
import struct
import zlib

ROOT=Path(__file__).resolve().parents[1]/'TvSat'
BG=(12,14,16,255); PANEL=(25,28,32,255); GREEN=(0,230,118,255)
SELECTED=(28,53,43,255)
WHITE=(245,245,245,255); RED=(255,98,98,255); BLUE=(94,172,255,255)


def png(path,w,h,bg,rects=()):
    pixels=bytearray(bg*(w*h))
    for x,y,rw,rh,c in rects:
        for yy in range(max(0,y),min(h,y+rh)):
            for xx in range(max(0,x),min(w,x+rw)):
                pixels[(yy*w+xx)*4:(yy*w+xx)*4+4]=bytes(c)
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    raw=b''.join(b'\0'+bytes(pixels[y*w*4:(y+1)*w*4]) for y in range(h))
    data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
    path=ROOT/path; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)


def build():
    # Neutralne tło: żaden symbol nie może prześwitywać przez przezroczyste logo.
    png(Path('picon_default.png'),220,132,PANEL)
    for name,c in [('timeline',PANEL),('timeline-now',GREEN),('state',GREEN)]:
        png(Path('assets')/(name+'.png'),4,4,c)
    for name,c in [('question',GREEN),('info',BLUE),('warning',(245,206,85,255)),('error',RED),('message',WHITE)]:
        png(Path('assets')/(name+'.png'),80,80,PANEL,[(35,15,10,34,c),(35,58,10,10,c)])
    normal=['CurrentEvent','OtherEvent','CurrentService','OtherService','TimeLineDate','TimeLineTime']
    selected=['SelectedCurrentEvent','SelectedEvent','SelectedZapEvent']
    for name in normal+selected+['RecordEvent','SelectedRecordEvent','RecordingEvent','ZapEvent']:
        c=SELECTED if name in selected else RED if 'Record' in name else BLUE if name=='ZapEvent' else PANEL
        png(Path('epg')/(name+'.png'),8,8,c)
    for name in ['BorderTop','BorderBottom','BorderLeft','BorderRight','SelectedBorderTop','SelectedBorderBottom','SelectedBorderLeft','SelectedBorderRight']:
        png(Path('epg')/(name+'.png'),2,2,BG)
    for name in ['information','SelectedInformation']:
        png(Path('epg')/(name+'.png'),24,24,PANEL,[(10,4,4,3,GREEN),(10,10,4,10,GREEN)])
    names=['epgclock','epgclock_add','epgclock_pre','epgclock_post','epgclock_prepost','epgclock_selpre','epgclock_selpost','epgclock_selprepost',
        'epgclock_zap','epgclock_zaprec','epgclock_autotimer','epgclock_disabled','epgclock_icetv','epgclock_primetime',
        'timer_autotimer','timer_done','timer_failed','timer_icetv','timer_off','timer_once','timer_prep','timer_rec','timer_rep','timer_wait','timer_zap',
        'folder','trashcan','movie_play','movie_play_rec','part_new','part_unwatched']+[f'part_{i}_4' for i in range(5)]
    for name in names:
        c=RED if any(k in name for k in ('rec','failed')) else BLUE if 'zap' in name else GREEN
        if 'folder' in name:
            rects=[(3,8,26,20,c),(3,4,12,6,c)]
        elif name=='trashcan':
            rects=[(7,10,18,20,c),(4,6,24,3,c)]
        elif name.startswith('part_'):
            part=int(name.split('_')[1]) if name.split('_')[1].isdigit() else 0
            rects=[(2,22,28,6,PANEL),(2,22,int(28*part/4),6,c)]
        else:
            rects=[(2,2,28,2,c),(2,28,28,2,c),(2,2,2,28,c),(28,2,2,28,c),(15,8,2,9,c),(15,15,9,2,c)]
        png(Path('icons')/(name+'.png'),32,32,(0,0,0,0),rects)
    # OpenATV ładuje mainmenu/<key>.png i używa missing.png dla nieznanych wtyczek.
    for i,name in enumerate(['missing','mainmenu','setup','information','timermenu','timer_edit','powertimer_edit','movie_selection','plugin_selection','shutdown','standby','restart','restart_enigma','deep_standby','epg','video_menu','audio_menu','system','user_interface','scan','service_searching','rec','network','hardisk_selection']):
        if name in ('mainmenu','movie_selection','video_menu'):
            rects=[(28,42,144,8,WHITE),(28,128,144,8,WHITE),(28,42,8,94,WHITE),(164,42,8,94,WHITE),(86,148,28,8,GREEN)]
        elif name in ('timermenu','timer_edit','powertimer_edit'):
            rects=[(36,36,128,8,WHITE),(36,156,128,8,WHITE),(36,36,8,128,WHITE),(156,36,8,128,WHITE),(96,56,8,52,GREEN),(96,100,42,8,GREEN)]
        elif name=='epg':
            rects=[(24,36+i*36,152,6,WHITE) for i in range(4)]+[(60,32,6,132,GREEN)]
        else:
            rects=[(42,42,44,44,WHITE),(114,42,44,44,GREEN),(42,114,44,44,GREEN),(114,114,44,44,WHITE)]
        png(Path('mainmenu')/(name+'.png'),200,200,(0,0,0,0),rects)
    print('Built picon fallback, timelines, EPG textures and system icons')


if __name__=='__main__':
    build()
