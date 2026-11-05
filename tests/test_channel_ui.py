from pathlib import Path
import unittest
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]


class ChannelUI(unittest.TestCase):
    def setUp(self):self.skin=E.parse(ROOT/'TvSat/skin.xml').getroot()

    def test_default_and_selected_styles_have_live_preview(self):
        for name in ('ChannelSelection','ChannelSelection_PIG'):
            screen=self.skin.find(f"screen[@name='{name}']")
            video=screen.find("widget[@render='Pig']")
            self.assertIsNotNone(video,name)
            w,h=map(int,video.get('size').split(','))
            self.assertGreaterEqual(w,600)
            self.assertEqual(w*9,h*16)
            self.assertEqual(video.get('source'),'session.VideoPicture')
            self.assertEqual(video.get('backgroundColor'),'transparent')
            vx,vy=map(int,video.get('position').split(','))
            # No later-created opaque decoration can cover the video aperture.
            for n in screen:
                if n.tag not in ('eLabel','ePixmap') or not n.get('backgroundColor'):continue
                x,y=map(int,n.get('position').split(','));nw,nh=map(int,n.get('size').split(','))
                overlaps=x<vx+w and x+nw>vx and y<vy+h and y+nh>vy
                self.assertFalse(overlaps,(name,n.attrib))

    def test_seven_rows_and_separate_channel_and_event_columns(self):
        screen=self.skin.find("screen[@name='ChannelSelection']")
        _,height=map(int,screen.find("widget[@name='list']").get('size').split(','))
        template=E.parse(ROOT/'TvSat/skinTemplates.xml').getroot().find('template')
        mode=template.find("mode[@name='services']")
        self.assertEqual(height//int(mode.get('itemHeight')),7)
        self.assertEqual(mode.get('foregroundColorSelected'),'white')
        self.assertEqual(mode.get('backgroundColorSelected'),'selected')
        stripe=mode.find('rectangle')
        self.assertEqual(stripe.get('foregroundColorSelected'),'green')
        title=mode.find("text[@index='ServiceName']");event=mode.find("text[@index='Title1']")
        self.assertLessEqual(int(title.get('position').split(',')[0])+int(title.get('size').split(',')[0]),int(event.get('position').split(',')[0]))
        self.assertEqual(title.get('wrap'),'ellipsis')
        self.assertEqual(event.get('wrap'),'ellipsis')
        self.assertIsNotNone(mode.find("progress[@index='Progress']"))

    def test_font_is_registered_regular_instead_of_default_bold(self):
        fonts={n.get('name'):n.get('filename') for n in self.skin.findall('fonts/font')}
        self.assertEqual(fonts['TvSatText'],'DejaVuSans.ttf')
        listbox=self.skin.find("screen[@name='ChannelSelection']/widget[@name='list']")
        self.assertTrue(listbox.get('serviceNameFont').startswith('TvSatText;'))
        self.assertGreaterEqual(int(listbox.get('serviceNameFont').split(';')[1]),30)

    def test_explicit_no_video_variant_remains_available(self):
        screen=self.skin.find("screen[@name='ChannelSelection_NoPIG']")
        self.assertIsNotNone(screen)
        self.assertIsNone(screen.find("widget[@render='Pig']"))

    def test_selected_event_description_has_room_before_info_hint(self):
        for name in ('ChannelSelection','ChannelSelection_PIG'):
            screen=self.skin.find(f"screen[@name='{name}']")
            description=next(n for n in screen.findall("widget[@source='ServiceEvent']")
                if n.find("convert[@type='EventName']") is not None and n.find("convert[@type='EventName']").text=='ExtendedDescription')
            height=int(description.get('size').split(',')[1])
            self.assertGreaterEqual(height,110)
            hint=next(n for n in screen.findall('eLabel') if n.get('text')=='INFO — pełny opis')
            bottom=int(description.get('position').split(',')[1])+height
            self.assertGreaterEqual(int(hint.get('position').split(',')[1])-bottom,8)


if __name__=='__main__':unittest.main()
