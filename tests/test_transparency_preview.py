from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from skin_colors import rgba
import preview


class TransparencyPreview(unittest.TestCase):
    def test_svg_and_png_show_video_through_bar_and_picon_area(self):
        from PIL import Image
        self.assertEqual(rgba('#180c0e10'),(12,14,16,231))
        with tempfile.TemporaryDirectory() as temp:
            svg=Path(temp)/'preview.svg'
            preview.render('InfoBar',str(svg),make_png=True)
            tree=E.parse(svg).getroot()
            rect=next(n for n in tree.iter() if n.tag.endswith('rect') and n.get('fill')=='#0c0e10')
            self.assertAlmostEqual(float(rect.get('fill-opacity')),231/255,places=6)
            with Image.open(svg.with_suffix('.png')) as image:
                def pixel(x,y):return image.getpixel((round(x*2/3),round(y*2/3)))
                colors=[]
                for x,y in ((160,1068),(900,1068),(1640,1068),(80,780)):
                    video=pixel(x,700)
                    expected=tuple(round(f*231/255+b*24/255) for f,b in zip((12,14,16),video))
                    actual=pixel(x,y)
                    self.assertTrue(all(abs(a-b)<=1 for a,b in zip(actual,expected)),(actual,expected))
                    colors.append(actual)
                self.assertEqual(len(set(colors[:3])),3,'Different TV colors must remain visible through the bar')


if __name__=='__main__':unittest.main()
