# Gör hjälpfiler för ChatGPT av en Blender-rendering (transparent bakgrund).
# python3 prep_x.py <render.png> <nyckel> <utmapp> [platshållarscen.png]
# X_bild = bara telefonen (resten transparent), X_mask = samma alfa (transparent = får ändras),
# X_topp = telefonen som klistras tillbaka över ChatGPT:s bild (så att skalet aldrig ritas om).
import sys
import numpy as np
from PIL import Image, ImageFilter

src, k, ut = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert('RGBA').resize((1008, 1792), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)
alfa = a[..., 3]
prod = (alfa > 245).astype(np.uint8) * 255          # bara själva telefonen, inte skuggan
m = Image.fromarray(prod).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
bild = im.copy(); bild.putalpha(Image.fromarray(prod))
if len(sys.argv) > 4:  # platshållarscen (block/podium/bord) som ChatGPT ska måla om
    bild = Image.open(sys.argv[4]).convert('RGBA').resize((1008, 1792), Image.LANCZOS)
bild.save(f'{ut}/X_bild_{k}.png')
mask = Image.new('RGBA', bild.size, (0, 0, 0, 0)); mask.putalpha(Image.fromarray(prod)); mask.save(f'{ut}/X_mask_{k}.png')
topp = im.copy(); topp.putalpha(m); topp.save(f'{ut}/X_topp_{k}.png')
print('ok', k)
