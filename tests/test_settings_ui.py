from pathlib import Path
import unittest
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]


class SettingsUI(unittest.TestCase):
    def test_setting_names_and_values_share_a_readable_font(self):
        skin=E.parse(ROOT/'TvSat/skin.xml').getroot()
        fonts={n.get('name') for n in skin.findall('fonts/font')}
        defaults=skin.find('windowstyle/configList')
        self.assertEqual(defaults.get('entryFont'),defaults.get('valueFont'))
        for widget in skin.findall(".//widget[@name='config']"):
            with self.subTest(screen_font=widget.get('font')):
                family,size=widget.get('valueFont').split(';')
                self.assertIn(family,fonts)
                self.assertGreaterEqual(int(size),28)
                self.assertEqual(widget.get('font'),widget.get('valueFont'))
                self.assertGreaterEqual(int(widget.get('itemHeight')),int(size)+20)
        setup=skin.find("screen[@name='Setup']/widget[@name='config']")
        self.assertEqual(int(setup.get('size').split(',')[1])%int(setup.get('itemHeight')),0)

    def test_infobar_has_one_lighter_opaque_surface(self):
        skin=E.parse(ROOT/'TvSat/skin.xml').getroot()
        colors={n.get('name'):n.get('value') for n in skin.findall('colors/color')}
        for name in ('InfoBar','SecondInfoBar'):
            screen=skin.find(f"screen[@name='{name}']")
            surface=colors[screen.get('backgroundColor')].lstrip('#')
            self.assertEqual(surface[:2],'00')
            rgb=[int(surface[i:i+2],16) for i in (2,4,6)]
            background=colors['bg'].lstrip('#')
            self.assertGreater(sum(rgb),sum(int(background[i:i+2],16) for i in (2,4,6)))
            for icon in screen.findall("widget[@render='Picon']"):
                self.assertEqual(icon.get('backgroundColor'),'transparent')
                self.assertEqual(icon.get('transparent'),'1')


if __name__=='__main__':
    unittest.main()
