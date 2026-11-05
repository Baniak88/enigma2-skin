from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as E
import base64
import io

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from skin_colors import rgba
import preview


class TransparencyPreview(unittest.TestCase):
    def test_svg_and_png_show_video_through_bar_and_picon_area(self):
        from PIL import Image
        self.assertEqual(rgba('#260c0e10'),(12,14,16,217))
        with tempfile.TemporaryDirectory() as temp:
            svg=Path(temp)/'preview.svg'
            preview.render('InfoBar',str(svg),make_png=True)
            tree=E.parse(svg).getroot()
            background=next(n for n in tree.iter() if n.tag.endswith('image') and n.get('width')=='1920' and n.get('height')=='418')
            with Image.open(io.BytesIO(base64.b64decode(background.get('href').split(',')[1]))) as mask:
                self.assertEqual(mask.getpixel((0,0)),(12,14,16,0))
                self.assertEqual(mask.getpixel((0,32)),(12,14,16,108))
                self.assertEqual(mask.getpixel((0,64)),(12,14,16,217))
            with Image.open(svg.with_suffix('.png')) as image:
                def pixel(x,y):return image.getpixel((round(x*2/3),round(y*2/3)))
                colors=[]
                for x,y in ((160,1068),(900,1068),(1640,1068),(80,780)):
                    self.assertEqual(image.getpixel((round(x*2/3),round(y*2/3)))[3],255,'Composited TV preview must remain opaque')
                    video=pixel(x,500)
                    expected=tuple(round(f*217/255+b*38/255) for f,b in zip((12,14,16),video))
                    actual=pixel(x,y)
                    self.assertTrue(all(abs(a-b)<=1 for a,b in zip(actual,expected)),(actual,expected))
                    colors.append(actual)
                self.assertEqual(len(set(colors[:3])),3,'Different TV colors must remain visible through the bar')
                # Fade above the body, away from the accent; all text stays below.
                video=pixel(900,500)
                self.assertTrue(all(abs(a-b)<=1 for a,b in zip(pixel(900,662),video)))
                # LANCZOS maps this sample between two source scanlines; check
                # the transition against its endpoints instead of rounding y.
                for middle,top,body in zip(pixel(900,694)[:3],video[:3],pixel(900,1068)[:3]):
                    self.assertGreater(middle,min(top,body))
                    self.assertLess(middle,max(top,body))

    def test_fade_never_runs_under_text_and_background_never_covers_picons(self):
        from PIL import Image
        for folder in ('TvSat','TvSatLarge'):
            skin=E.parse(ROOT/folder/'skin.xml').getroot()
            for name in ('InfoBar','SecondInfoBar','MoviePlayer'):
                scene=skin.find(f"screen[@name='{name}']")
                background=scene.find(f"ePixmap[@pixmap='TvSat/assets/{name.lower()}-fade.png']")
                with Image.open(ROOT/background.get('pixmap')) as mask:
                    alpha=[mask.getpixel((0,y))[3] for y in range(mask.height)]
                    self.assertEqual(alpha,sorted(alpha))
                    for node in scene:
                        if node.get('font'):
                            y=int(node.get('position').split(',')[1])
                            self.assertGreaterEqual(alpha[y],217,(folder,name,node.attrib))
                for logo in scene.findall("widget[@render='Picon']"):
                    self.assertGreater(int(logo.get('zPosition')),int(background.get('zPosition')))


if __name__=='__main__':unittest.main()
