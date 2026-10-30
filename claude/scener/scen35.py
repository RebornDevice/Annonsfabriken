# Ref 35 (Mous "Perfect Match"): telefonen svävar över en mörk klippa mot blå himmel, småsten flyger.
import bpy, math, mathutils, random
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
p = [23.912, 17.2916, -10.9093, 133.506, -0.0053831, -0.1069183]
FARG = globals().get('FARG', 'blue')
L['ny_scen'](1080, 1920); r = L['telefon'](FARG, p); L['material_fix'](); L['kamera'](p, 1080, 1920)
L['gradient']((0.02, 0.035, 0.07), (0.25, 0.4, 0.6), amb=0.12)
sten, snt, sb = L['nmat']('sten'); sb.inputs['Base Color'].default_value = (0.02, 0.024, 0.032, 1); sb.inputs['Roughness'].default_value = 0.8
sv = L['koord'](snt); sn = snt.nodes.new('ShaderNodeTexNoise'); sn.inputs['Scale'].default_value = 150; sn.inputs['Detail'].default_value = 14; sn.inputs['Roughness'].default_value = 0.7; snt.links.new(sv, sn.inputs['Vector']); L['bump'](snt, sb, sn.outputs['Fac'], 1.0, 0.006)
farg = L['ramp'](snt, sn.outputs['Fac'], [(0.35, (0.006, 0.007, 0.01)), (0.65, (0.04, 0.045, 0.055))]); snt.links.new(farg, sb.inputs['Base Color'])
def klippa(namn, loc, skala, styrka, seed, sub=5):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1); o = bpy.context.object; bpy.ops.object.shade_smooth(); o.name = namn; o.parent = r
    o.location = loc; o.scale = skala
    tx = bpy.data.textures.new(namn + 'tx', 'VORONOI'); tx.noise_scale = 0.5; tx.distance_metric = 'DISTANCE'
    dp = o.modifiers.new('d', 'DISPLACE'); dp.texture = tx; dp.strength = styrka
    tx2 = bpy.data.textures.new(namn + 'tx2', 'CLOUDS'); tx2.noise_scale = 0.07; tx2.noise_depth = 8; tx2.noise_type = 'HARD_NOISE'
    dp2 = o.modifiers.new('d2', 'DISPLACE'); dp2.texture = tx2; dp2.strength = styrka * 0.5
    o.data.materials.append(sten); return o
klippa('klippa', (0.06, -0.0827 - 0.068, 0.03), (0.17, 0.06, 0.07), 0.3, 1, sub=7)
klippa('klippa2', (-0.15, -0.0827 - 0.11, 0.02), (0.12, 0.07, 0.07), 0.3, 2, sub=6)
random.seed(4)
for i, (x, y) in enumerate([(0.07, -0.06), (-0.06, -0.09), (0.09, -0.02), (-0.08, -0.05), (0.05, -0.1), (0.1, -0.08), (0.06, -0.075), (0.085, -0.045), (-0.045, -0.075), (0.11, -0.03), (-0.07, -0.1)]):
    s = random.uniform(0.004, 0.009)
    o = klippa('sten%d' % i, (x, y, random.uniform(-0.02, 0.03)), (s, s * 0.8, s * 0.7), 0.45, i, sub=3)
    o.rotation_euler = (random.random() * 3, random.random() * 3, random.random() * 3)
for nm, lok, e, s, *f in [('nyckel', (-0.4, 0.3, 0.5), 18, 0.8, (0.85, 0.92, 1.0)), ('kant', (0.45, 0.35, -0.2), 30, 0.5, (0.7, 0.85, 1.0)), ('fyll', (0.1, -0.2, 0.7), 4, 1.5)]:
    L['lokalt_ljus'](r, nm, lok, e, s, *(f or [(1, 1, 1)]))
cam = bpy.context.scene.camera; cam.data.dof.use_dof = True; cam.data.dof.focus_distance = 1.0; cam.data.dof.aperture_fstop = 11
