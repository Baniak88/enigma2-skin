"""Build complete Standard/Large skins, sharing graphics through TvSat paths."""
import ast
from copy import deepcopy
import xml.etree.ElementTree as E


def write_xml(path,root):
    path.parent.mkdir(parents=True,exist_ok=True)
    E.indent(root,space='  ')
    path.write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n'+E.tostring(root,encoding='utf-8')+b'\n')


def service_templates(large=False):
    root=E.Element('templates')
    name='TvSatLarge' if large else 'TvSat'
    height=116 if large else 100
    template=E.SubElement(root,'template',name=name,component='serviceList',fonts='TvSatText;38,TvSatText;32,TvSatText;30' if large else 'TvSatText;31,TvSatText;26,TvSatText;26')
    def item(mode,tag,**attrs):
        return E.SubElement(mode,tag,{k:str(v) for k,v in attrs.items()})
    for kind in ('services','bouquets','other'):
        mode=E.SubElement(template,'mode',name=kind,itemHeight=str(height),itemWidth='1088',foregroundColor='white',foregroundColorSelected='white',backgroundColor='bg',backgroundColorSelected='selected')
        item(mode,'rectangle',position='0,0',size=f'4,{height}',foregroundColor='bg',foregroundColorSelected='green')
        item(mode,'rectangle',position=f'8,{height-1}',size='1080,1',foregroundColor='line',foregroundColorSelected='selected')
        if kind=='other':
            item(mode,'text',index='EntryName',position='24,0',size=f'1040,{height}',font='0',verticalAlignment='center',wrap='ellipsis')
            continue
        item(mode,'text',index='Number',position='12,0',size=f'56,{height}',font='2',horizontalAlignment='right',verticalAlignment='center',foregroundColor='muted',foregroundColorSelected='white')
        item(mode,'pixmap',index='Picon',position=f'84,{(height-56)//2}',size='100,56',alpha='blend',scale='scaleCenter')
        item(mode,'text',index='ServiceName',position='204,8' if large else '204,0',size='860,50' if large else f'420,{height}',font='0',verticalAlignment='center',wrap='ellipsis')
        item(mode,'text',index='Title1',position='204,66' if large else '648,0',size='748,42' if large else f'304,{height}',font='1',verticalAlignment='center',foregroundColor='muted',foregroundColorSelected='white',wrap='ellipsis')
        item(mode,'progress',index='Progress',position='980,84' if large else '980,46',size='88,8',foregroundColor='green',foregroundColorSelected='green',backgroundColor='line',backgroundColorSelected='line',borderWidth='0')
    return root


def bigger_height(value):
    return ((int(value)*6//5+7)//8)*8


def enlarge_template(code):
    tree=ast.parse(code,mode='eval')
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
            if node.func.id=='gFont':node.args[1].value+=4
            elif node.func.id.startswith('MultiContentEntry'):
                for kw in node.keywords:
                    if kw.arg=='pos':kw.value.elts[1].value=round(kw.value.elts[1].value*1.2)
                    elif kw.arg=='size':kw.value.elts[1].value=bigger_height(kw.value.elts[1].value)
        if isinstance(node,ast.Dict):
            for key,val in zip(node.keys,node.values):
                if isinstance(key,ast.Constant) and key.value=='itemHeight':val.value=bigger_height(val.value)
                if isinstance(key,ast.Constant) and key.value=='templates':
                    for style in val.values:style.elts[0].value=bigger_height(style.elts[0].value)
    return ast.unparse(tree)


def large_skin(skin):
    large=deepcopy(skin)
    for node in large.iter():
        for key,value in list(node.attrib.items()):
            if key.lower().endswith('font') and ';' in value:
                family,size=value.rsplit(';',1)
                node.set(key,f'{family};{int(size)+4}')
        if node.tag=='alias':
            node.set('size',str(int(node.get('size'))+4))
            node.set('height',str(bigger_height(node.get('height'))))
        if node.tag=='widget':
            if node.get('itemHeight'):
                node.set('itemHeight',str(bigger_height(node.get('itemHeight'))))
                width,height=map(int,node.get('size').split(','))
                row=int(node.get('itemHeight'))
                if height>=row:node.set('size',f'{width},{height//row*row}')
            if node.get('NumberOfRows'):
                node.set('NumberOfRows',str(max(3,int(node.get('NumberOfRows'))-2)))
            converter=node.find("convert[@type='TemplatedMultiContent']")
            if converter is not None:
                converter.text=enlarge_template(converter.text)
                from validate import check_template
                template=check_template(converter.text)
                row=template.get('itemHeight') or template['templates']['default'][0]
                width,height=map(int,node.get('size').split(','))
                if height>=row:node.set('size',f'{width},{height//row*row}')
    for name in ('ChannelSelection','ChannelSelection_PIG','ChannelSelection_NoPIG','ChannelSelectionRadio'):
        screen=large.find(f"screen[@name='{name}']")
        if screen.get('label'):screen.set('label',screen.get('label').replace('TvSat','TvSat Large'))
        widget=screen.find("widget[@name='list']")
        widget.set('size','1088,696');widget.set('serviceItemHeight','116')
    # Keep short labels tall enough for the enlarged baseline/descenders.
    for scene in large.findall('screen'):
        screen_height=int(scene.get('size').split(',')[1])
        for node in scene:
            if node.get('font'):
                font=int(node.get('font').rsplit(';',1)[1])
                width,height=map(int,node.get('size').split(','))
                y=int(node.get('position').split(',')[1])
                minimum=(font*6+4)//5
                if height<minimum and y+minimum<=screen_height:node.set('size',f'{width},{minimum}')
    # 8 full file rows become 6 full 80px rows; keep native aliases in sync.
    for side in ('left','right'):
        node=large.find(f"screen[@name='FileCommander']/widget[@name='list{side}']")
        node.set('itemHeight','80');node.set('size','864,480')
    for alias in large.findall('fonts/alias'):
        if alias.get('name') in ('FileList','FileListMulti'):alias.set('height','80')
    # Keep generic settings at eight 80px rows, and skin settings at seven.
    for node in large.findall(".//widget[@name='config']"):
        width,height=map(int,node.get('size').split(','));row=int(node.get('itemHeight'))
        if height>=row:node.set('size',f'{width},{height//row*row}')
    return large


def write_variants(root,skin):
    write_xml(root/'TvSat/skinTemplates.xml',service_templates())
    write_xml(root/'TvSatLarge/skin.xml',large_skin(skin))
    write_xml(root/'TvSatLarge/skinTemplates.xml',service_templates(True))
