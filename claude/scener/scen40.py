# Ref 40: reklamskylt på en glasfasad i stan, kameran nerifrån. DEL='stad' (staden med magenta skylt) eller 'tel' (bara telefonen)
import bpy, math, mathutils, random
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
W, H = 960, 1200
p = [-2.0493, 16.219, -39.188, 120.298, -0.016220, -0.0044963]
if DEL == 'tel':
    L['ny_scen'](W, H); r = L['telefon'](globals().get('FARG', 'white'), p); L['material_fix'](); L['kamera'](p, W, H)
    for nm, lok, e, s, *f in [('nyckel', (-0.3, 0.4, 0.5), 16, 1.0), ('kant', (0.4, 0.3, -0.1), 8, 0.5), ('fyll', (0.1, -0.2, 0.7), 5, 2)]:
        L['lokalt_ljus'](r, nm, lok, e, s, *(f or [(1, 1, 1)]))
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.8, 0.82, 0.86, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.5
else:
    L['ny_scen'](W, H); s = bpy.context.scene
    c = bpy.data.cameras.new('cam'); c.lens = 24; c.sensor_fit = 'VERTICAL'; c.sensor_height = 24
    o = bpy.data.objects.new('cam', c); s.collection.objects.link(o); s.camera = o; o.location = (0, -8, 1.6); c.shift_y = 0.457
    o.rotation_euler = (math.radians(90), 0, 0)
    w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True
    wn = w.node_tree; bgn = wn.nodes['Background']; bgn.inputs['Strength'].default_value = 1.2
    env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load('/Applications/Blender.app/Contents/Resources/5.0/datafiles/studiolights/world/city.exr')
    wn.links.new(env.outputs['Color'], bgn.inputs['Color'])
    himmel = wn.nodes.new('ShaderNodeBackground'); himmel.inputs['Color'].default_value = (0.62, 0.68, 0.76, 1); himmel.inputs['Strength'].default_value = 1.3
    lp = wn.nodes.new('ShaderNodeLightPath'); mx = wn.nodes.new('ShaderNodeMixShader')
    wn.links.new(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); wn.links.new(bgn.outputs[0], mx.inputs[1]); wn.links.new(himmel.outputs[0], mx.inputs[2])
    wn.links.new(mx.outputs[0], wn.nodes['World Output'].inputs['Surface'])
    def glas(namn, farg, skala):
        m, nt, b = L['nmat'](namn); v = L['koord'](nt)
        br = nt.nodes.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = skala; br.offset = 0.0; br.inputs['Mortar Size'].default_value = 0.06
        br.inputs['Brick Width'].default_value = 1.6; br.inputs['Row Height'].default_value = 1.1
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (math.radians(90), 0, 0)
        tc = nt.nodes.new('ShaderNodeNewGeometry'); nt.links.new(tc.outputs['Position'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], br.inputs['Vector'])
        ns = nt.nodes.new('ShaderNodeTexNoise'); ns.inputs['Scale'].default_value = 0.05; nt.links.new(tc.outputs['Position'], ns.inputs['Vector'])
        gl = L['ramp'](nt, ns.outputs['Fac'], [(0.3, tuple(x * 0.6 for x in farg)), (0.7, tuple(x * 1.4 for x in farg))])
        br.inputs['Mortar'].default_value = (0.03, 0.03, 0.035, 1); nt.links.new(gl, br.inputs['Color1']); nt.links.new(gl, br.inputs['Color2'])
        nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
        rm = L['ramp'](nt, br.outputs['Fac'], [(0.0, (0.05, 0.05, 0.05)), (0.5, (0.6, 0.6, 0.6))]); nt.links.new(rm, b.inputs['Roughness'])
        b.inputs['Metallic'].default_value = 0.9; return m
    def lada(namn, loc, dim, rot, mat):
        bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object; o.name = namn; o.location = loc; o.scale = dim
        o.rotation_euler = [math.radians(a) for a in rot]; o.data.materials.append(mat); return o
    g1 = glas('glas1', (0.08, 0.1, 0.13), 1.0); g2 = glas('glas2', (0.12, 0.14, 0.17), 1.3)
    lada('fasad', (0, 14, 25), (16, 1, 50), (0, 0, 0), g1)
    lada('vanster', (-10.5, 6, 35), (6, 22, 70), (0, 0, -4), g2)
    lada('hoger', (10.5, 18, 30), (6, 8, 60), (0, 0, 6), g2)
    lada('hoger2', (19, 40, 45), (8, 10, 90), (0, 0, 5), g1)
    lada('gata', (0, 10, -0.05), (60, 60, 0.1), (0, 0, 0), L['mat_enkel']((0.04, 0.04, 0.045), 0.6))
    ent = lada('entre', (0, 13.4, 1.7), (14, 0.3, 3.4), (0, 0, 0), glas('lobby', (0.05, 0.05, 0.05), 1.0))
    lb = bpy.data.materials['lobby'].node_tree.nodes['Principled BSDF']; lb.inputs['Emission Color'].default_value = (1, 0.78, 0.55, 1); lb.inputs['Emission Strength'].default_value = 0.35
    m = bpy.data.materials.new('skylt'); m.use_nodes = True; n = m.node_tree.nodes; e = n.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (1, 0, 1, 1); e.inputs['Strength'].default_value = 1
    m.node_tree.links.new(e.outputs[0], n['Material Output'].inputs['Surface'])
    bpy.ops.mesh.primitive_plane_add(size=1); sk = bpy.context.object; sk.name = 'skylt'; sk.rotation_euler = (math.radians(90), 0, 0)
    sk.location = (0, 13.35, 13.6); sk.scale = (10.3, 20.7, 1); sk.data.materials.append(m)
    ram = lada('ram', (0, 13.42, 13.6), (10.8, 0.1, 21.3), (0, 0, 0), L['mat_enkel']((0.02, 0.02, 0.022), 0.3, 0.5))
    sol = bpy.data.lights.new('sol', 'SUN'); sol.energy = 2; so = bpy.data.objects.new('sol', sol); s.collection.objects.link(so); so.rotation_euler = (math.radians(40), 0, math.radians(30))
    s.view_settings.look = 'AgX - Medium High Contrast'
