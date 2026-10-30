# Skrivbordsscen (ref 11). Kör i Blender: FARG='white'; exec(open(...scen11.py).read())
import bpy, math, mathutils, random
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
V = mathutils.Vector; B = L['bild_till_mark']
p = [-26.881, -29.960, 37.523, 140.089, -0.018119, -0.010547]
def matta():
    m, nt, b = L['nmat']('matta'); v = L['koord'](nt)
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 1500; n.inputs['Detail'].default_value = 2; nt.links.new(v, n.inputs['Vector'])
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 15; nt.links.new(v, n2.inputs['Vector'])
    c = L['ramp'](nt, n2.outputs['Fac'], [(0.3, (0.012, 0.012, 0.014)), (0.7, (0.022, 0.022, 0.026))]); nt.links.new(c, b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.85; L['bump'](nt, b, n.outputs['Fac'], 0.4, 0.0005); return m
r = L['ligger'](FARG, p, 1080, 1080, matta, ljus=[('nyckel', (-0.1, 0.5, 0.6), 12, 0.9), ('fyll', (0.4, -0.3, 0.5), 2, 1.5)], amb=0.05)
mark = bpy.data.objects['mark']
dark = L['mat_enkel']((0.008, 0.008, 0.01), 0.45)
def em(col, s):
    m = bpy.data.materials.new('em'); m.use_nodes = True; n = m.node_tree.nodes; e = n.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (*col, 1); e.inputs['Strength'].default_value = s
    m.node_tree.links.new(e.outputs[0], n['Material Output'].inputs['Surface']); return m
glow = bpy.data.materials.new('glow'); glow.use_nodes = True; gn = glow.node_tree.nodes; e = gn.new('ShaderNodeEmission'); e.inputs['Strength'].default_value = 6
tc = gn.new('ShaderNodeTexCoord'); sep = gn.new('ShaderNodeSeparateXYZ'); rp = gn.new('ShaderNodeValToRGB')
glow.node_tree.links.new(tc.outputs['Generated'], sep.inputs[0]); glow.node_tree.links.new(sep.outputs['X'], rp.inputs['Fac'])
rp.color_ramp.elements[0].color = (1, 0.05, 0.08, 1); rp.color_ramp.elements[1].color = (0.1, 0.25, 1, 1)
glow.node_tree.links.new(rp.outputs['Color'], e.inputs['Color']); glow.node_tree.links.new(e.outputs[0], gn['Material Output'].inputs['Surface'])
red = em((1, 0.08, 0.1), 3); blue = em((0.15, 0.35, 1), 3)
def obj(o, loc, rotz=0, mat=None):
    o.parent = mark; o.location = loc; o.rotation_euler = (0, 0, rotz)
    if mat: o.data.materials.append(mat)
    return o
a = V(B(0.0, 0.0)); b_ = V(B(1.0, 0.0)); d = (b_ - a).normalized(); ang = math.atan2(d.y, d.x)
up = (V(B(0.5, 0.0)) - V(B(0.5, 0.1))).normalized()
start = V(B(-0.04, 0.10)); s = 0.0185; g = 0.0205
kc = start + d * 0.2 + up * 0.03
bpy.ops.mesh.primitive_cube_add(size=1); kb = obj(bpy.context.object, (kc.x, kc.y, 0.009), ang, dark); kb.scale = (0.55, 0.11, 0.018)
bv = kb.modifiers.new('b', 'BEVEL'); bv.width = 0.004; bv.segments = 4
for j in range(4):
    for i in range(24):
        pos = start + d * (i * g) + up * (j * g)
        bpy.ops.mesh.primitive_cube_add(size=1); k = obj(bpy.context.object, (pos.x, pos.y, 0.022), ang, dark); k.scale = (s, s, 0.008)
        bv = k.modifiers.new('b', 'BEVEL'); bv.width = 0.0025; bv.segments = 3
        bpy.ops.mesh.primitive_plane_add(size=1); gp = obj(bpy.context.object, (pos.x, pos.y, 0.0181), ang, glow); gp.scale = (g, g, 1)
        bpy.ops.mesh.primitive_plane_add(size=1); lg = obj(bpy.context.object, (pos.x, pos.y, 0.0262), ang, red if i < 12 else blue); lg.scale = (s * 0.35, s * 0.18, 1)
h = V(B(0.02, 0.66))
bpy.ops.mesh.primitive_cylinder_add(radius=0.034, depth=0.03, vertices=96); e1 = obj(bpy.context.object, (h.x, h.y, 0.015), 0, dark); bpy.ops.object.shade_smooth()
bv = e1.modifiers.new('b', 'BEVEL'); bv.width = 0.008; bv.segments = 6
bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.008, major_segments=96, minor_segments=16); t = bpy.context.object; t.parent = mark
c = V(B(-0.3, 0.42)); t.location = (c.x, c.y, 0.008); t.data.materials.append(dark); bpy.ops.object.shade_smooth()
la = V(B(0.97, 0.3))
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=64, ring_count=32); lf = obj(bpy.context.object, (la.x, la.y, 0.0), ang + math.radians(-60), L['mat_enkel']((0.30, 0.11, 0.04), 0.45)); lf.scale = (0.12, 0.05, 0.04); bpy.ops.object.shade_smooth()
p0 = V(B(0.72, 0.33)); p1 = V(B(0.99, 0.72)); pd = p1 - p0; pm = (p0 + p1) / 2
bpy.ops.mesh.primitive_cylinder_add(radius=0.0065, depth=pd.length, vertices=48); pe = bpy.context.object; bpy.ops.object.shade_smooth(); pe.parent = mark; pe.location = (pm.x, pm.y, 0.0068)
pe.rotation_euler = (math.radians(90), 0, math.atan2(pd.y, pd.x) - math.radians(90)); pe.data.materials.append(L['mat_enkel']((0.6, 0.6, 0.58), 0.35))
cp = p0 + pd.normalized() * 0.022
bpy.ops.mesh.primitive_cylinder_add(radius=0.0072, depth=0.045, vertices=48); ca = bpy.context.object; bpy.ops.object.shade_smooth(); ca.parent = mark; ca.location = (cp.x, cp.y, 0.0072)
ca.rotation_euler = pe.rotation_euler; ca.data.materials.append(dark)
