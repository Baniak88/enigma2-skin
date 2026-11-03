from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate import check_picon_layers


class PiconLayers(unittest.TestCase):
    def test_original_blank_panel_regression(self):
        # Order in XML did not help: OpenATV creates the eLabel after Picon.
        original=E.fromstring('''<screen name="InfoBar">
          <eLabel position="64,34" size="220,132" backgroundColor="panel"/>
          <widget source="session.CurrentService" render="Picon" position="64,34" size="220,132"/>
        </screen>''')
        with self.assertRaisesRegex(AssertionError,'decoration covers picon'):
            check_picon_layers(original)

    def test_shipped_picons_above_fallback(self):
        screens=E.parse(ROOT/'CanalPL/skin.xml').getroot().findall('screen')
        count=0
        for screen in screens:
            check_picon_layers(screen)
            for picon in screen.findall("widget[@render='Picon']"):
                count+=1
                matching=[n for n in screen.findall('ePixmap')
                    if n.get('position')==picon.get('position') and n.get('size')==picon.get('size')]
                self.assertTrue(matching,screen.get('name'))
                for fallback in matching:
                    self.assertEqual(fallback.get('pixmap'),'CanalPL/picon_default.png')
                    self.assertLess(int(fallback.get('zPosition','0')),int(picon.get('zPosition','0')))
        self.assertGreater(count,10)


if __name__=='__main__':unittest.main()
