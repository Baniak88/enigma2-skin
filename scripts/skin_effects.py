"""Static, native PNG effects. Fade stays above every text/control rectangle."""
import xml.etree.ElementTree as E

FADE_TOP=64
BODY_ALPHA=217  # ~85% opacity, retaining the requested ~15% transparency.
BODY_RGB=(12,14,16)
BAR_HEIGHTS={'InfoBar':354,'SecondInfoBar':504,'MoviePlayer':294}


def fade_alpha(y):
    t=min(1,max(0,y/FADE_TOP))
    return round(BODY_ALPHA*t*t*(3-2*t))


def pixmap(parent,path,x,y,w,h,z):
    node=E.Element('ePixmap',position=f'{x},{y}',size=f'{w},{h}',pixmap=f'TvSat/assets/{path}',scale='1',alphatest='blend',zPosition=str(z))
    parent.insert(0,node)
    return node


def modernize_bars(skin):
    for name,height in BAR_HEIGHTS.items():
        scene=skin.find(f"screen[@name='{name}']")
        scene.set('position',f'0,{1080-height-FADE_TOP}')
        scene.set('size',f'1920,{height+FADE_TOP}')
        scene.set('backgroundColor','transparent')
        for node in list(scene):
            x,y=map(int,node.get('position').split(','))
            if node.tag=='eLabel' and (x,y)==(64,0) and node.get('backgroundColor')=='green':
                scene.remove(node)
                continue
            node.set('position',f'{x},{y+FADE_TOP}')
        # Native Screen creates decorations after renderers: explicit negative
        # z puts the surface behind text/Picon regardless of creation order.
        pixmap(scene,'accent-fade.png',64,FADE_TOP,1792,2,-5)
        pixmap(scene,'accent-glow.png',64,FADE_TOP-8,1792,18,-6)
        pixmap(scene,f'{name.lower()}-fade.png',0,0,1920,height+FADE_TOP,-10)
        if name=='InfoBar':
            pixmap(scene,'now-badge.png',308,FADE_TOP+104,128,48,-4)
            E.SubElement(scene,'eLabel',position=f'304,{FADE_TOP+34}',size='1,142',backgroundColor='line')
            for widget in scene.findall("widget[@source='session.CurrentService']"):
                if widget.get('render')=='Label':widget.set('font','TvSatStrong;38')
