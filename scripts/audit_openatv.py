#!/usr/bin/env python3
"""Odczytuje AST źródeł OpenATV, bez importowania/wykonywania ich kodu.

Użycie: python3 scripts/audit_openatv.py /tmp/canalpl-openatv --write
Wymaga checkoutów 7.5 i 7.6 w podkatalogach argumentu.
Zapisany kontrakt pozwala ponawiać kontrolę bez sieci i bez odbiornika.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def callname(node):
    if isinstance(node,ast.IfExp):
        return callname(node.body) or callname(node.orelse)
    if isinstance(node,ast.Call):
        if isinstance(node.func,ast.Name):
            return node.func.id
        if isinstance(node.func,ast.Attribute):
            return node.func.attr
    return None


def subkey(node):
    if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='self':
        if isinstance(node.slice,ast.Constant) and isinstance(node.slice.value,str):
            return node.slice.value
    return None


def extract(directory):
    classes={}; fingerprints={}
    for path in sorted((directory/'lib/python').rglob('*.py')):
        fingerprints[str(path.relative_to(directory))]=hashlib.sha256(path.read_bytes()).hexdigest()
        tree=ast.parse(path.read_text(),filename=str(path))
        for cls in [c for c in tree.body if isinstance(c,ast.ClassDef)]:
            entries={}; mandatory=[]
            for node in ast.walk(cls):
                if isinstance(node,ast.Assign):
                    kind=callname(node.value)
                    if kind:
                        for target in node.targets:
                            key=subkey(target)
                            if key:
                                entries.setdefault(key,kind)
                if isinstance(node,ast.Call):
                    for kw in node.keywords:
                        if kw.arg=='mandatoryWidgets' and isinstance(kw.value,ast.List):
                            mandatory += [x.value for x in kw.value.elts if isinstance(x,ast.Constant)]
            data={'module':path.name,'bases':[b.id for b in cls.bases if isinstance(b,ast.Name)],'widgets':entries,'required':mandatory}
            classes[cls.name]=data
            classes[path.name+':'+cls.name]=data
    def inherited(name,seen=None):
        seen=set() if seen is None else seen
        if name not in classes and ':' in name:
            name=name.split(':')[-1]
        if name in seen or name not in classes:
            return {},[]
        seen.add(name); c=classes[name]; result={}; required=[]
        for base in c['bases']:
            w,r=inherited(c['module']+':'+base,seen);result.update(w);required+=r
        result.update(c['widgets']);required+=c['required']
        return result,required
    mapping={
        'Menu':'Menu','ChannelSelection':'ChannelSelection','ChannelSelection_PIG':'ChannelSelection',
        'ChannelSelectionRadio':'ChannelSelectionRadio','SimpleChannelSelection':'SimpleChannelSelection','SlimChannelSelection':'SimpleChannelSelection',
        'BouquetSelector':'BouquetSelector','EPGBouquetSelector':'EPGBouquetSelector',
        **{x:'EPGSelection' for x in ['EPGSelection','QuickEPG','EPGSelectionMulti','GraphicalEPG','GraphicalEPGPIG','GraphicalInfoBarEPG','EPGvertical','EPGverticalPIG']},
        'EventView':'EventViewEPGSelect','InfoBarEventView':'EventViewSimple','Setup':'Setup',
        'ChoiceBox':'ChoiceBoxNew','ChannelContextMenu':'ChannelContextMenu','MessageBox':'MessageBox','MessageBoxSimple':'MessageBox',
        'MovieSelection':'MovieSelection','MovieSelectionSlim':'MovieSelection',
        'TimerOverview':'RecordTimerOverview','RecordTimerOverview':'RecordTimerOverview','TimerEditList':'RecordTimerOverview',
        'PluginBrowserList':'PluginBrowser','PluginBrowserGrid':'PluginBrowser','InfoBar':'InfoBar','SecondInfoBar':'SecondInfoBar',
        'MoviePlayer':'MoviePlayer','PVRState':'PVRState','TimeshiftState':'TimeshiftState','NumberZap':'NumberZap'
        ,'AudioSelection':'AudioSelection','QuickSubtitlesConfigMenu':'QuickSubtitlesConfigMenu'
    }
    screens={}
    for screen,cls in mapping.items():
        widgets,required=inherited(cls)
        widgets.update(inherited('Screen')[0])
        if cls=='PluginBrowser':
            widgets.update(pluginList='List',pluginGrid='List')  # self[self.layout]
        if cls=='EPGSelection':
            widgets.update({f'timeline{i}':'Pixmap' for i in range(6)})  # f-string loop
        screens[screen]={'class':cls,'widgets':widgets,'required':sorted(set(required))}
    # Volume/Mute to core Enigma2 screens (C++), only these fixed widgets.
    screens['Volume']={'class':'C++ Volume','widgets':{'Volume':'ProgressBar'},'required':['Volume']}
    screens['Mute']={'class':'C++ Mute','widgets':{},'required':[]}
    return {'source_sha256':fingerprints,'screens':screens}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('sources',type=Path);parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result={version:extract(args.sources/version) for version in ('7.5','7.6')}
    if args.write:
        target=ROOT/'scripts/openatv-contracts.json'
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(target)
    else:
        known=json.loads((ROOT/'scripts/openatv-contracts.json').read_text())
        assert result==known,'Kontrakt różni się od zapisanych źródeł'
        print('OpenATV source contracts match')
