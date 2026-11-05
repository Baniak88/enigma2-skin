#!/usr/bin/env python3
"""Run original XML template parsers; replace only C++ geometry/fonts/colors.

Checks both native service/bouquet modes, indices, centering, ellipsis, progress
and picon scaling. Does not decode services or prove rendering on hardware.
"""
import argparse
import ast
from contextlib import redirect_stdout
import io
from pathlib import Path
from types import SimpleNamespace as NS
from urllib.request import urlopen
import xml.etree.ElementTree as E
from check_upstream_fonts import PINS,ROOT


class Context:
    def __init__(self,*args):pass
    def parse(self,position,size,font=None):
        return tuple(map(int,position.split(','))),tuple(map(int,size.split(',')))


def definition(source,name):
    return next(n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)


def probe(version,skin_source,list_source):
    colors={n.get('name'):int(n.get('value').lstrip('#'),16) for n in E.parse(ROOT/'TvSat/skin.xml').getroot().findall('colors/color')}
    def parse_color(value):
        result=colors[value] if value in colors else int(value.lstrip('#'),16)
        return NS(argb=lambda:result)
    ns={'eListboxPythonMultiContent':NS(TYPE_PIXMAP_ALPHABLEND=1,TYPE_PIXMAP_ALPHATEST=2,TYPE_PIXMAP=3),
        'parseColor':parse_color,'parseFont':lambda font:NS(family=font.split(';')[0],pointSize=int(font.split(';')[1])),
        'SkinContext':Context,'SkinContextStack':Context,'SizeTuple':tuple,'skinError':lambda text:(_ for _ in ()).throw(AssertionError(text))}
    scale=definition(skin_source,'parseScale')
    constants=sorted({n.id for n in ast.walk(scale) if isinstance(n,ast.Name) and n.id.startswith('BT_')})
    ns.update({name:1<<index for index,name in enumerate(constants)})
    nodes=[definition(skin_source,'parseOptions'),scale,definition(skin_source,'TemplateParser'),definition(list_source,'ServiceListTemplateParser')]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'native-service-template','exec'),ns)
    field=lambda value:NS(value=value)
    ns['config']=NS(channelSelection=NS(recordIndicatorMode=field(1),showPicon=field(True),piconRatio=field(180),showNumber=field(True),showServiceTypeIcon=field(False),showCryptoIcon=field(False)),usage=NS(numberMode=field(2),servicelist_column=field('-1')))
    for directory in ('TvSat','TvSatLarge'):
        template=E.parse(ROOT/directory/'skinTemplates.xml').getroot().find('template')
        ns['getcomponentTemplate']=lambda component,name:template
        instance=ns['ServiceListTemplateParser']()
        instance.l=NS(setFont=lambda *args:None)
        instance.listHeight=700;instance.listWidth=1088
        errors=io.StringIO()
        with redirect_stdout(errors):instance.readTemplate(directory)
        assert not errors.getvalue(),errors.getvalue()
        for items in (instance.templateDataServices,instance.templateDataBouquets):
            by_index={item.get('index'):item for item in items if 'index' in item}
            assert {0,1,2,50,101}<=set(by_index),(directory,set(by_index))
            assert by_index[1]['_flags'] & 128 and by_index[1]['_flags'] & 16,by_index[1]
            assert by_index[101]['_flags'] & 128 and by_index[101]['_flags'] & 16
            assert by_index[2]['pixmapFlags']>0,'Picons must scale while keeping aspect ratio'
            assert by_index[50]['type']=='progress'
    print(f'OpenATV {version}: original Standard/Large service templates: modes, EPG indices, ellipsis, centering and picon scaling pass (C++ stubbed).')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('sources',type=Path,nargs='?');parser.add_argument('--download',action='store_true');args=parser.parse_args()
    if args.sources is None and not args.download:parser.error('provide snapshots or --download')
    for version,pin in PINS.items():
        sources=[]
        for path in ('lib/python/skin.py','lib/python/Components/ServiceList.py'):
            if args.sources:sources.append((args.sources/version/path).read_text())
            else:
                with urlopen(f'https://raw.githubusercontent.com/openatv/enigma2/{pin}/{path}',timeout=30) as response:sources.append(response.read().decode())
        probe(version,*sources)


if __name__=='__main__':main()
