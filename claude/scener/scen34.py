# Ref 34 (Native Union ReClassic): telefonen står på ett draperat plommonfärgat tyg mot plommonvägg.
import bpy, math, mathutils
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
p = [24.385, 3.0434, 5.1946, 124.74, 0.010009, -0.02758]
FARG = globals().get('FARG', 'black')
r = L['star'](FARG, p, 1080, 1080, ljus=[('nyckel', (-0.4, 0.25, 0.35), 14, 0.7, (1, 0.85, 0.95)), ('kant', (0.4, 0.3, -0.15), 10, 0.4, (1, 0.7, 0.9)), ('fyll', (0.1, 0.0, 0.7), 2, 1.5)], amb=0.02)
bpy.data.objects.remove(bpy.data.objects['golv'], do_unlink=True)
def tyg(namn, farg, sheen):
    m, nt, b = L['nmat'](namn); v = L['koord'](nt)
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 900; n.inputs['Detail'].default_value = 3; nt.links.new(v, n.inputs['Vector'])
    b.inputs['Base Color'].default_value = (*farg, 1); b.inputs['Roughness'].default_value = 0.8
    b.inputs['Sheen Weight'].default_value = sheen; b.inputs['Sheen Tint'].default_value = (1, 0.7, 0.9, 1)
    L['bump'](nt, b, n.outputs['Fac'], 0.25, 0.0005); return m
# rundat podium klätt i tyg
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.3, vertices=128); g = bpy.context.object; g.parent = r
g.rotation_euler = (math.radians(90), 0, 0); g.location = (0.0, -0.0829 - 0.15, 0.035 - 0.3)
bv = g.modifiers.new('b', 'BEVEL'); bv.width = 0.02; bv.segments = 8; bv.limit_method = 'ANGLE'
sub = g.modifiers.new('s', 'SUBSURF'); sub.levels = 1; sub.render_levels = 1
tx = bpy.data.textures.new('veck', 'CLOUDS'); tx.noise_scale = 0.4; tx.noise_depth = 1
dp = g.modifiers.new('d', 'DISPLACE'); dp.texture = tx; dp.strength = 0.006
bpy.ops.object.shade_smooth(); g.data.materials.append(tyg('tyg', (0.009, 0.0025, 0.007), 0.4))
# vägg
L['plan']('vagg', 4, (0, 0, -0.12), (0, 0, 0), r, tyg('vagg', (0.02, 0.006, 0.017), 0.25))
