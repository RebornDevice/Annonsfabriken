"""Beskär PNG-renderingar tätt runt produkten (behåller genomskinligheten)."""
import sys
from PIL import Image
for p in sys.argv[1:]:
    im = Image.open(p).convert('RGBA')
    box = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    if not box: continue
    m = int(max(box[2]-box[0], box[3]-box[1]) * 0.03)
    box = (max(0, box[0]-m), max(0, box[1]-m), min(im.width, box[2]+m), min(im.height, box[3]+m))
    im.crop(box).save(p, optimize=True)
    print('beskuren', p, im.crop(box).size)
