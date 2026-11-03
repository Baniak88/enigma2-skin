#!/usr/bin/env python3
"""Autorskie układy, nazwy widgetów zgodne z OpenATV 7.5/7.6.

Źródło API opisane w docs/COMPATIBILITY.md. Nie kopiuje kodu Python Enigma2.
"""
from pathlib import Path
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
PALETTE = dict(bg='0c0e10', panel='191c20', white='f5f5f5', muted='a5adb6',
               green='00e676', line='30363d', red='ff6262', yellow='f5ce55', blue='5eacff')
skin = E.Element('skin')


def add(parent, tag, **attrs):
    return E.SubElement(parent, tag, {k: str(v) for k, v in attrs.items() if v is not None})


def box(s, x, y, w, h, color='line', **kw):
    return add(s, 'eLabel', position=f'{x},{y}', size=f'{w},{h}', backgroundColor=color, **kw)


def label(s, text, x, y, w, h, font=28, color='white', **kw):
    return add(s, 'eLabel', text=text, position=f'{x},{y}', size=f'{w},{h}',
               font=f'Regular;{font}', foregroundColor=color, transparent='1', **kw)


def widget(s, name, x, y, w, h, font=None, **kw):
    return add(s, 'widget', name=name, position=f'{x},{y}', size=f'{w},{h}',
               font=f'Regular;{font}' if font else None, **kw)


def source(s, name, x, y, w, h, font=28, color='white', render='Label', converts=(), **kw):
    if render != 'Picon':
        kw.setdefault('foregroundColor', color)
    n = add(s, 'widget', source=name, render=render, position=f'{x},{y}', size=f'{w},{h}',
            font=f'Regular;{font}' if render in ('Label', 'FixedLabel') else None,
            transparent='1' if render in ('Label', 'FixedLabel') else None, **kw)
    for kind, arg in converts:
        add(n, 'convert', type=kind).text = arg
    return n


def screen(name, pos=(0, 0), size=(1920, 1080), bg='bg'):
    return add(skin, 'screen', name=name, position=f'{pos[0]},{pos[1]}',
               size=f'{size[0]},{size[1]}', flags='wfNoBorder', backgroundColor=bg)


def header(s, section):
    label(s, 'CANALPL', 64, 38, 320, 60, 42)
    label(s, section, 420, 46, 1110, 48, 28, 'green')
    source(s, 'global.CurrentTime', 1600, 40, 256, 58, 38, halign='right', converts=[('ClockToText', 'Default')])
    box(s, 64, 126, 1792, 3, 'green')
    source(s, 'Title', 64, 150, 1792, 52, 32, 'muted', noWrap='1')


def footer(s, keys=('red', 'green', 'yellow', 'blue')):
    box(s, 64, 974, 1792, 2)
    for i, key in enumerate(keys):
        x = 64 + i * 448
        box(s, x, 1012, 6, 24, key)
        source(s, f'key_{key}', x + 22, 998, 414, 50, 25, noWrap='1', valign='center', conditional=f'key_{key}')


LIST = dict(backgroundColor='bg', foregroundColor='white',
            backgroundColorSelected='green', foregroundColorSelected='bg', scrollbarMode='showOnDemand')


def picon(s, src, x, y, w=220, h=132):
    box(s, x, y, w, h, 'panel')
    return source(s, src, x, y, w, h, render='Picon', converts=[('ServiceName', 'Reference')], alphatest='blend')


def event(s, src, x, y, w, desc=True):
    source(s, src, x, y, w, 54, 34, converts=[('EventName', 'Name')], noWrap='1')
    source(s, src, x, y+66, 140, 42, 26, 'green', converts=[('EventTime', 'StartTime'), ('ClockToText', 'Default')])
    source(s, src, x+144, y+66, 160, 42, 26, 'muted', converts=[('EventTime', 'EndTime'), ('ClockToText', 'Format:– %H:%M')])
    if desc:
        source(s, src, x, y+132, w, 186, 26, 'muted', converts=[('EventName', 'ExtendedDescription')])


def templated(n, template):
    add(n, 'convert', type='TemplatedMultiContent').text = template


def build():
    add(add(skin, 'output', id='0'), 'resolution', xres='1920', yres='1080', bpp='32')
    colors = add(skin, 'colors')
    for name, value in PALETTE.items():
        add(colors, 'color', name=name, value='#00'+value)
    add(colors, 'color', name='overlay', value='#100c0e10')
    add(colors, 'color', name='transparent', value='#ff000000')
    style = add(skin, 'windowstyle', type='skinned', id='0')
    add(style, 'title', offset='24,12', font='Regular;30')
    for name, color in dict(Background='bg', LabelForeground='white', ListboxBackground='bg', ListboxForeground='white',
        ListboxSelectedBackground='green', ListboxSelectedForeground='bg', ListboxMarkedBackground='panel',
        ListboxMarkedForeground='green', ListboxMarkedAndSelectedBackground='green',
        ListboxMarkedAndSelectedForeground='bg', WindowTitleForeground='white', WindowTitleBackground='bg').items():
        add(style, 'color', name=name, color=color)
    fonts = add(skin, 'fonts')
    for name, size, height in [('TextNormal',30,40), ('ChoiceBoxDescription',26,36), ('MenuFont',32,64)]:
        add(fonts, 'alias', name=name, font='Regular', size=size, height=height)

    s = screen('Menu'); header(s, 'MENU'); footer(s)
    n = source(s, 'menu', 64, 240, 1080, 640, render='Listbox', **LIST)
    common = 'MultiContentEntryText(pos=(92,0),size=(950,80),font=0,flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER,text=3)'
    icon = 'MultiContentEntryPixmapAlphaBlend(pos=(16,12),size=(56,56),png=1,flags=BT_SCALE|BT_KEEP_ASPECT_RATIO)'
    number = 'MultiContentEntryText(pos=(12,0),size=(60,80),font=1,flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER,text=2)'
    templated(n, '{"fonts":[gFont("Regular",32),gFont("Regular",26)],"templates":{' +
        ','.join('"%s":(80,[%s])' % (k, v) for k,v in {
            'default': 'MultiContentEntryText(pos=(24,0),size=(1030,80),font=0,flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER,text=0)',
            'text':common, 'number':number+','+common, 'image':icon+','+common,
            'both':icon+','+'MultiContentEntryText(pos=(92,0),size=(60,80),font=1,flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER,text=2),MultiContentEntryText(pos=(168,0),size=(870,80),font=0,flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER,text=3)'
        }.items()) + '}}')
    box(s, 1200, 240, 2, 640)
    widget(s, 'menuimage', 1390, 248, 240, 240, alphatest='blend', scale='1')
    source(s, 'description', 1264, 540, 592, 266, 32, 'muted')
    label(s, 'OK  Wybierz     EXIT  Powrót', 64, 906, 1080, 42, 24, 'muted')

    for name in ('ChannelSelection','ChannelSelection_PIG','ChannelSelectionRadio'):
        s = screen(name); header(s, 'TELEWIZJA / BUKIETY' if name != 'ChannelSelectionRadio' else 'RADIO / BUKIETY'); footer(s)
        s.set('base','ChannelSelection'); s.set('label','CanalPL — '+('podgląd TV' if name.endswith('PIG') else 'lista'))
        widget(s, 'list', 64, 236, 1160, 684, serviceNameFont='Regular;29', serviceInfoFont='Regular;24',
            serviceNumberFont='Regular;26', serviceItemHeight='68', foregroundColorEvent='muted',
            foregroundColorEventSelected='bg', colorEventProgressbar='green', colorEventProgressbarSelected='bg', **LIST)
        box(s, 1260, 236, 2, 684)
        picon(s, 'ServiceEvent', 1312, 236)
        source(s, 'ServiceEvent', 1312, 390, 544, 48, 30, 'green', converts=[('ServiceName','Name')], noWrap='1')
        event(s, 'ServiceEvent', 1312, 464, 544)
        if name == 'ChannelSelection_PIG':
            # Wariant PIG: obraz zamiast opisu; układ listy pozostaje taki sam.
            s.remove(s[-1])
            source(s, 'session.VideoPicture', 1312, 642, 544, 306, render='Pig', backgroundColor='transparent', zPosition='2')

    for name in ('SimpleChannelSelection','SlimChannelSelection'):
        s=screen(name); header(s,'WYBIERZ KANAŁ / BUKIET'); footer(s)
        widget(s,'list',64,236,1792,684,serviceNameFont='Regular;30',serviceInfoFont='Regular;25',serviceNumberFont='Regular;26',serviceItemHeight='68',**LIST)

    for name in ('BouquetSelector','EPGBouquetSelector'):
        s=screen(name); header(s,'WYBÓR BUKIETU'); footer(s,('red','green'))
        widget(s,'menu',64,240,1120,640,32,itemHeight='80',**LIST)
        box(s,1248,240,2,640)
        label(s,'TWOJE KANAŁY',1312,260,544,70,38,'green')
        label(s,'Wybierz bukiet z listy.\n\nOK — otwórz\nEXIT — wróć',1312,372,544,300,30,'muted')

    epg_attrs=dict(ServiceFontGraphical='Regular;26',EntryFontGraphical='Regular;26',ServiceFontInfobar='Regular;26',
        EventFontInfobar='Regular;26',EventFontSingle='Regular;29',EventFontMulti='Regular;28',EventFontVertical='Regular;25',
        TimeFontVertical='Regular;23',ServiceForegroundColor='white',ServiceForegroundColorNow='green',ServiceBackgroundColor='panel',
        ServiceBackgroundColorNow='panel',EntryForegroundColor='white',EntryForegroundColorSelected='bg',EntryBackgroundColor='panel',
        EntryBackgroundColorSelected='green',EntryBackgroundColorNow='panel',EntryBackgroundColorNowSelected='green',
        EntryForegroundColorNow='white',EntryForegroundColorNowSelected='bg',EntryBackgroundColorPast='bg',
        EntryBackgroundColorPastSelected='green',EntryForegroundColorPast='muted',EntryForegroundColorPastSelected='bg',
        EntryBorderColor='bg',ServiceBorderColor='bg',ServiceBorderWidth='2',EventBorderWidth='2',EventNamePadding='12',
        ServiceNamePadding='12',RecordForegroundColor='white',RecordForegroundColorSelected='white',RecordBackgroundColor='red',
        RecordBackgroundColorSelected='red',ZapForegroundColor='white',ZapBackgroundColor='blue',ZapForegroundColorSelected='bg',ZapBackgroundColorSelected='green')
    for name in ('EPGSelection','QuickEPG','EPGSelectionMulti','GraphicalEPG','GraphicalEPGPIG','GraphicalInfoBarEPG'):
        s=screen(name); header(s,'PROGRAM TV'); footer(s)
        graph=name.startswith('Graphical')
        pig=name=='GraphicalEPGPIG'
        multi=name=='EPGSelectionMulti'
        if graph:
            event(s,'Event',64,218,1200 if pig else 1792,desc=False)
            if pig:
                source(s,'session.VideoPicture',1376,208,480,270,render='Pig',backgroundColor='transparent',zPosition='2')
            y=506 if pig else 366
            height=420 if pig else 560
            widget(s,'timeline_text',64,y-46,1792,46,TimelineFont='Regular;26',itemHeight='46',foregroundColor='muted',backgroundColor='bg')
            widget(s,'list',64,y,1792,height,NumberOfRows='6' if pig else '8',**epg_attrs,**LIST)
            widget(s,'lab1',64,y,1792,height,32,halign='center',valign='center',backgroundColor='bg',zPosition='5')
            for i in range(6):
                widget(s,f'timeline{i}',64,y,2,height,pixmap='CanalPL/assets/timeline.png',scale='1',zPosition='2')
            widget(s,'timeline_now',64,y,4,height,pixmap='CanalPL/assets/timeline-now.png',scale='1',zPosition='3')
            widget(s,'bouquetlist',64,y,720,height,30,itemHeight='70',zPosition='4',**LIST)
        else:
            if multi:
                for i,part in enumerate(('now','next','more')):
                    widget(s,part+'_button',64+i*240,216,224,48,pixmap='CanalPL/epg/OtherEvent.png')
                    widget(s,part+'_button_sel',64+i*240,216,224,48,pixmap='CanalPL/epg/SelectedEvent.png',zPosition='1')
                    widget(s,part+'_text',76+i*240,222,200,40,25,transparent='1',zPosition='2',halign='center')
                widget(s,'date',1440,216,416,48,26,halign='right',transparent='1')
            else:
                source(s,'Service',64,216,1792,54,32,'green',converts=[('ServiceName','Name')],noWrap='1')
            widget(s,'list',64,300,1160,616,NumberOfRows='8',**epg_attrs,**LIST)
            widget(s,'lab1',64,300,1160,616,30,backgroundColor='bg',halign='center',valign='center',zPosition='5')
            picon(s,'Service',1312,280)
            event(s,'Event',1312,456,544)
            if multi:
                widget(s,'bouquetlist',64,300,720,616,30,itemHeight='70',zPosition='4',**LIST)
        widget(s,'number',1660,214,196,48,30,foregroundColor='green',halign='right',transparent='1',zPosition='6')

    for name in ('EPGvertical','EPGverticalPIG'):
        s=screen(name); header(s,'PROGRAM TV / UKŁAD PIONOWY'); footer(s)
        pig=name.endswith('PIG'); count=3 if pig else 5
        width=416 if pig else 344
        for i in range(1,count+1):
            x=64+(i-1)*(width+16)
            picon(s,f'piconCh{i}',x,230,132,80)
            widget(s,f'currCh{i}',x+144,240,width-144,54,24,transparent='1')
            widget(s,f'Active{i}',x,322,width,4,backgroundColor='green')
            widget(s,f'list{i}',x,344,width,434,NumberOfRows='6',**epg_attrs,**LIST)
        widget(s,'list',64,212,1,1,scrollbarMode='showNever')
        widget(s,'bouquetlist',64,344,720,434,30,itemHeight='62',zPosition='4',**LIST)
        widget(s,'lab1',64,344,1280 if pig else 1792,434,32,backgroundColor='bg',zPosition='5',halign='center',valign='center')
        source(s,'Event',64,814,1792,50,30,converts=[('EventName','Name')],noWrap='1')
        source(s,'Event',64,878,1792,72,25,'muted',converts=[('EventName','ExtendedDescription')])
        if pig:
            source(s,'session.VideoPicture',1440,230,416,234,render='Pig',backgroundColor='transparent',zPosition='2')

    for name in ('EventView','InfoBarEventView'):
        s=screen(name); header(s,'INFORMACJE O AUDYCJI'); footer(s)
        widget(s,'channel',64,224,1792,54,32,foregroundColor='green',transparent='1')
        widget(s,'datetime',64,298,1100,44,26,foregroundColor='muted',transparent='1')
        widget(s,'duration',1440,298,416,44,26,foregroundColor='muted',transparent='1',halign='right')
        widget(s,'epg_description',64,388,1792,550,32,transparent='1')

    s=screen('Setup'); header(s,'USTAWIENIA'); footer(s)
    widget(s,'config',64,236,1160,672,30,itemHeight='56',**LIST)
    box(s,1260,236,2,672)
    widget(s,'description',1312,246,544,530,30,foregroundColor='muted',transparent='1')
    widget(s,'footnote',1312,810,544,108,26,foregroundColor='yellow',transparent='1')
    widget(s,'HelpWindow',64,240,1,1,conditional='HelpWindow',transparent='1')

    for name in ('ChoiceBox','ChannelContextMenu'):
        s=screen(name); header(s,'OPCJE')
        if name=='ChoiceBox':
            widget(s,'text',64,220,1792,130,30,transparent='1')
            widget(s,'list',64,376,1792,560,32,itemHeight='64',**LIST)
        else:
            footer(s)
            widget(s,'menu',64,236,1792,684,32,itemHeight='64',**LIST)

    for name in ('MessageBox','MessageBoxSimple'):
        s=screen(name,pos=(320,200),size=(1280,680))
        box(s,0,0,1280,4,'green')
        source(s,'Title',40,32,1200,58,36)
        widget(s,'icon',40,132,80,80,pixmaps=','.join('CanalPL/assets/'+x+'.png' for x in ('question','info','warning','error','message')),conditional='icon',alphatest='blend',scale='1')
        widget(s,'text',160,132,1080,344,30,transparent='1')
        widget(s,'list',40,508,1200,128,30,itemHeight='64',**LIST)

    for name in ('MovieSelection','MovieSelectionSlim'):
        s=screen(name); header(s,'NAGRANIA'); footer(s)
        widget(s,'list',64,236,1160,650,30,**LIST)
        widget(s,'waitingtext',64,236,1160,650,32,halign='center',valign='center',backgroundColor='bg',zPosition='5')
        widget(s,'chosenletter',64,236,1160,650,80,halign='center',valign='center',foregroundColor='green',transparent='1',zPosition='6')
        # OpenATV odwołuje się do instance DescriptionBorder przy zmianie trybu opisu.
        # Wąska niewidoczna ramka zachowuje wymagany obiekt bez panelu pod listą.
        widget(s,'DescriptionBorder',64,236,1,1,pixmap='CanalPL/assets/state.png',alphatest='blend')
        source(s,'Service',1312,236,544,140,32,converts=[('MovieInfo','ShortDescription')])
        source(s,'Service',1312,412,544,50,26,'green',converts=[('MovieInfo','RecordServiceName')])
        source(s,'Service',1312,508,544,340,27,'muted',converts=[('EventName','ExtendedDescription')])
        widget(s,'freeDiskSpace',64,916,1792,40,25,foregroundColor='muted',transparent='1',halign='right')
        for i,key in enumerate(('movie_sort','movie_off')):
            widget(s,key,64+i*48,916,32,32,pixmaps=','.join(['CanalPL/assets/state.png']*10),alphatest='blend')

    for name in ('TimerOverview','RecordTimerOverview','TimerEditList'):
        s=screen(name); header(s,'ZAPLANOWANE NAGRANIA'); footer(s)
        widget(s,'timerlist',64,236,1792,560,**LIST)
        widget(s,'description',64,830,1792,116,28,foregroundColor='muted',transparent='1')

    for name in ('PluginBrowserList','PluginBrowserGrid'):
        s=screen(name); header(s,'WTYCZKI'); footer(s)
        grid=name.endswith('Grid'); key='pluginGrid' if grid else 'pluginList'
        n=source(s,key,64,236,1792,600,render='Listbox',listOrientation='grid' if grid else 'vertical',**LIST)
        tpl='[MultiContentEntryPixmapAlphaBlend(pos=(24,12),size=(100,60),png=3,flags=BT_SCALE|BT_KEEP_ASPECT_RATIO),MultiContentEntryText(pos=(156,4),size=(1580,42),font=0,flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER,text=1),MultiContentEntryText(pos=(156,48),size=(1580,40),font=1,text=2)]'
        if grid:
            tpl='[MultiContentEntryPixmapAlphaBlend(pos=(124,20),size=(100,60),png=3,flags=BT_SCALE|BT_KEEP_ASPECT_RATIO),MultiContentEntryText(pos=(12,100),size=(324,80),font=0,flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER|RT_WRAP,text=1)]'
        templated(n,'{"template":'+tpl+',"fonts":[gFont("Regular",30),gFont("Regular",24)],"itemHeight":'+('200,"itemWidth":352}' if grid else '100}'))
        widget(s,'quickselect',64,236,1792,600,80,halign='center',valign='center',transparent='1',foregroundColor='green',zPosition='5')
        widget(s,'description',64,860,1792,90,27,foregroundColor='muted',transparent='1')

    s=screen('AudioSelection'); header(s,'DŹWIĘK I NAPISY')
    widget(s,'config',112,236,1744,224,30,itemHeight='56',**LIST)
    widget(s,'switchdescription',64,484,1792,50,27,foregroundColor='muted',transparent='1')
    for i,key in enumerate(('red','green','yellow','blue')):
        source(s,'key_'+key,64,244+i*56,30,40,24,key,render='FixedLabel',text='●',converts=[('ConditionalShowHide',None)])
    entries='[MultiContentEntryText(pos=(20,0),size=(90,64),font=0,flags=RT_VALIGN_CENTER,text=2),MultiContentEntryText(pos=(130,0),size=(560,64),font=0,flags=RT_VALIGN_CENTER,text=3),MultiContentEntryText(pos=(720,0),size=(860,64),font=0,flags=RT_VALIGN_CENTER,text=4),MultiContentEntryText(pos=(1640,0),size=(100,64),font=0,flags=RT_VALIGN_CENTER,text=5)]'
    n=source(s,'streams',64,560,1792,384,render='Listbox',**LIST)
    templated(n,'{"fonts":[gFont("Regular",30)],"templates":{"default":(64,'+entries+',True,"showOnDemand"),"notselected":(64,'+entries+',False,"showOnDemand")}}')
    for i,key in enumerate(('key_left','key_right')):
        widget(s,key,64+i*40,484,24,24,pixmap='CanalPL/assets/state.png',alphatest='blend')
    s=screen('QuickSubtitlesConfigMenu'); header(s,'USTAWIENIA NAPISÓW')
    widget(s,'config',64,236,1792,616,30,itemHeight='56',**LIST)
    widget(s,'videofps',64,890,1792,48,26,foregroundColor='muted',transparent='1')

    s=screen('InfoBar',pos=(0,726),size=(1920,354),bg='overlay')
    box(s,64,0,1792,4,'green'); picon(s,'session.CurrentService',64,34)
    source(s,'session.CurrentService',320,28,1190,60,38,converts=[('ServiceName','Name')],noWrap='1')
    source(s,'global.CurrentTime',1570,28,286,60,40,halign='right',converts=[('ClockToText','Default')])
    label(s,'TERAZ',320,110,104,40,23,'green')
    source(s,'session.Event_Now',440,104,140,46,28,converts=[('EventTime','StartTime'),('ClockToText','Default')])
    source(s,'session.Event_Now',600,98,1256,54,34,converts=[('EventName','Name')],noWrap='1')
    source(s,'session.Event_Now',320,174,1536,6,render='Progress',color='green',converts=[('EventTime','Progress')],backgroundColor='line',borderWidth='0')
    label(s,'POTEM',320,214,104,40,23,'muted')
    source(s,'session.Event_Next',440,208,140,44,28,'muted',converts=[('EventTime','StartTime'),('ClockToText','Default')])
    source(s,'session.Event_Next',600,202,1256,54,30,'muted',converts=[('EventName','Name')],noWrap='1')
    source(s,'session.RecordState',64,290,240,38,24,'red',render='FixedLabel',text='NAGRYWANIE',converts=[('ConditionalShowHide','Blink')])
    source(s,'session.Event_Now',1556,290,300,38,24,'muted',halign='right',converts=[('EventTime','Remaining'),('RemainingToText','InMinutes')])

    s=screen('SecondInfoBar',pos=(0,576),size=(1920,504),bg='overlay')
    box(s,64,0,1792,4,'green'); picon(s,'session.CurrentService',64,34)
    source(s,'session.CurrentService',320,34,1536,56,36,'green',converts=[('ServiceName','Name')])
    event(s,'session.Event_Now',320,120,1536)

    s=screen('MoviePlayer',pos=(0,786),size=(1920,294),bg='overlay')
    box(s,64,0,1792,4,'green'); label(s,'ODTWARZANIE NAGRANIA',64,30,1792,42,26,'green')
    source(s,'session.CurrentService',64,100,1792,64,38,converts=[('ServiceName','Name')],noWrap='1')
    source(s,'session.CurrentService',64,208,230,48,28,converts=[('ServicePosition','Position')])
    source(s,'session.CurrentService',330,230,1180,6,render='Progress',color='green',backgroundColor='line',borderWidth='0',converts=[('ServicePosition','Position')])
    source(s,'session.CurrentService',1550,208,306,48,28,'muted',halign='right',converts=[('ServicePosition','Remaining,Negate')])
    widget(s,'state',1200,30,400,42,26,foregroundColor='green',transparent='1')
    widget(s,'speed',1640,30,216,42,26,transparent='1',halign='right')
    widget(s,'statusicon',0,0,1,1,pixmaps=','.join(['CanalPL/assets/state.png']*7),alphatest='blend')

    for name in ('PVRState','TimeshiftState'):
        s=screen(name,pos=(64,62),size=(540,176))
        widget(s,'state',24,18,320,62,34,foregroundColor='green',transparent='1')
        widget(s,'speed',366,18,150,62,30,transparent='1',halign='right')
        widget(s,'statusicon',0,0,1,1,pixmaps=','.join(['CanalPL/assets/state.png']*7),alphatest='blend')
        widget(s,'eventname',24,120,492,44,24,foregroundColor='muted',transparent='1')
        if name=='TimeshiftState':
            widget(s,'PTSSeekBack',24,96,492,6,pixmap='CanalPL/assets/timeline.png',scale='1')
            widget(s,'PTSSeekPointer',24,90,4,18,pixmap='CanalPL/assets/timeline-now.png',scale='1',zPosition='2')

    s=screen('NumberZap',pos=(1200,70),size=(656,164))
    box(s,0,0,6,164,'green')
    widget(s,'number',30,14,160,58,40,foregroundColor='green',transparent='1')
    widget(s,'servicename',30,88,596,50,28,transparent='1')
    s=screen('Volume',pos=(1356,70),size=(500,110))
    label(s,'GŁOŚNOŚĆ',28,16,444,36,24)
    widget(s,'Volume',28,74,444,8,foregroundColor='green',backgroundColor='line',borderWidth='0')
    s=screen('Mute',pos=(1496,70),size=(360,86))
    box(s,0,0,6,86,'green'); label(s,'WYCISZONO',30,22,300,44,28)
    E.indent(skin,space='  ')
    (ROOT/'CanalPL/skin.xml').write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n'+E.tostring(skin,encoding='utf-8')+b'\n')
    print(f'Generated {len(skin.findall("screen"))} OpenATV screens')


if __name__=='__main__':
    build()
