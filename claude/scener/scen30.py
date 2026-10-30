# Ref 30: fyra stående telefoner i diagonal rad (bakre till vänster), ljus studio. Främre = passad vinkel,
# övriga förskjutna i telefonens egna koordinater (OFF, meter: x bredd, y höjd, z djup mot kameran).
import bpy, math, mathutils
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
p = globals().get('P30', [0, 0, 0, 100, 0, 0])
FARGER = globals().get('FARGER', ['white', 'blue', 'orange', 'black'])  # främst -> bakerst
STEG = globals().get('STEG', (0.055, 0.0, -0.07))
VRID = globals().get('VRID', 0)
W = globals().get('BW', 1080); H = globals().get('BH', 1080)
r = L['star'](FARGER[0], p, W, H, ljus=[('nyckel', (-0.5, 0.35, 0.5), 30, 0.9), ('kant', (0.5, 0.3, -0.25), 12, 0.6), ('fyll', (0.15, 0.05, 0.7), 8, 1.5)], amb=0.6)
if globals().get('LIGG'):  # liggande telefoner: golvet = skärmens plan
    g = bpy.data.objects['golv']; g.location = (0, 0, globals().get('GOLVZ', -0.0003)); g.rotation_euler = (0, 0, 0)
bpy.context.view_layer.update(); R = r.matrix_world.to_3x3()
for i, f in enumerate(FARGER[1:], 1):
    off = R @ mathutils.Vector((STEG[0] * i, STEG[1] * i, STEG[2] * i))
    o = L['G']['importera'](L['GLB'][f], loc=tuple(off), rot=(90 + p[0], p[1], p[2]))
    if VRID and o is not None:  # extra lutning per steg runt telefonens normal (solfjäder)
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (R @ mathutils.Matrix.Rotation(math.radians(VRID * i), 3, 'Z')).to_quaternion()
L['material_fix']()
KD = globals().get('KAMAVST', 1.0)  # längre kameraavstånd = plattare perspektiv (samma bildutsnitt)
if KD != 1.0:
    c = bpy.context.scene.camera; c.location = (0, -KD, 0); c.data.lens *= KD
if globals().get('TYG'):  # bakgrund: mjukt skrynkligt vitt tyg (lakan), utan telefoner
    for o in list(bpy.data.objects):
        if o.type == 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.mesh.primitive_plane_add(size=1.2); t = bpy.context.object; t.parent = r; t.location = (0, 0, -0.004)
    bpy.ops.object.modifier_add(type='SUBSURF'); t.modifiers[-1].levels = 6; t.modifiers[-1].render_levels = 6; t.modifiers[-1].subdivision_type = 'SIMPLE'
    for sk, st, nm in [(0.07, 0.045, 'stor'), (0.025, 0.01, 'liten')]:
        tx = bpy.data.textures.new(nm, 'CLOUDS'); tx.noise_scale = sk; tx.noise_depth = 2
        d = t.modifiers.new(nm, 'DISPLACE'); d.texture = tx; d.strength = st; d.mid_level = 0.5
    bpy.ops.object.shade_smooth()
    m = L['mat_enkel']((0.8, 0.79, 0.77), 0.95); t.data.materials.append(m)
    for o in list(bpy.data.objects):
        if o.type == 'LIGHT': o.data.energy *= 0.35
    sl = bpy.data.lights.new('fonster', 'SUN'); sl.energy = 3.2; sl.angle = math.radians(6)
    so = bpy.data.objects.new('fonster', sl); bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = (R @ mathutils.Vector((-0.8, 0.5, -0.45))).to_track_quat('-Z', 'Y').to_euler()
