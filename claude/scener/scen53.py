# Ref 53: stående telefon rakt bakifrån i ljusgrå studio (sömlös bakgrund), mjuk skugga, mörk sten till vänster.
import bpy, math
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
FARG = globals().get('FARG', 'blue')
STEN = globals().get('STEN', True)
p = [5.519173825255079, -0.2067435507437549, 4.1397823997015415, 100.6, -0.0002, 0.0077]  # fit IoU .94, manuellt skalad till synlig kontur
W, H = 1080, 1920
gra = (0.78, 0.78, 0.79)
# golvet = skuggfångare; renderas transparent och läggs på ljus gradient i efterhand
r = L['star'](FARG, p, W, H,
              ljus=[('nyckel', (-0.45, 0.35, 0.5), 26, 0.9), ('kant', (0.45, 0.3, -0.2), 10, 0.6), ('fyll', (0.15, 0.05, 0.7), 8, 1.5)], amb=0.55)
w = bpy.context.scene.world
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.95, 0.95, 0.96, 1)
if STEN:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1); s = bpy.context.object; s.parent = r
    # liggande rundad sten framför-vänster om telefonen, på golvet (lokalt y=-0.0828 är golvet)
    s.scale = (0.027, 0.017, 0.021); s.location = (-0.06, -0.0828 + 0.0165, 0.035)
    bpy.ops.object.shade_smooth()
    m = L['mat_enkel']((0.01, 0.0095, 0.009), 0.9); s.data.materials.append(m)
