# Ref 28 (Native Union Active Case): fyra stående telefoner på ett bord, räfflad panel + stenplatta bakom.
# Kör i Blender: DEL='bg' (bakgrund från mittkameran) eller DEL='28_0'..'28_3' (en telefon + skugga), PCT, SAMPLES
import bpy, math, mathutils
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
P = {'28_0': ('black', [3.528, 1.4218, 16.965, 77.2, -0.232488, 0.119291]),
     '28_1': ('blue', [2.406, 0.8347, 18.461, 74.335, -0.052059, 0.104358]),
     '28_2': ('black', [7.78, 4.4999, 25.558, 73.464, 0.121361, 0.092957]),
     '28_3': ('white', [3.125, 1.7799, 29.298, 72.027, 0.283015, 0.082828])}
W = H = 1080
for _k, _f in (globals().get('FARGER') or {}).items(): P[_k] = (_f, P[_k][1])
def sol(r):
    s = bpy.data.lights.new('sol', 'SUN'); s.energy = 7.0; s.angle = math.radians(1.5); s.color = (1, 0.97, 0.93)
    o = bpy.data.objects.new('sol', s); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = mathutils.Vector((1.0, 0.55, -0.7)).to_track_quat('-Z', 'Y').to_euler()
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.7, 0.72, 0.75, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
if DEL == 'bg':
    farg, p = P['28_1']
    L['ny_scen'](W, H); r = L['telefon'](farg, p); L['kamera'](p, W, H)
    for o in list(bpy.data.objects):
        if o.type == 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    bord = L['mat_enkel']((0.16, 0.16, 0.165), 0.7)
    bpy.ops.mesh.primitive_cube_add(size=1); t = bpy.context.object; t.parent = r
    t.location = (0.05, -0.0828 - 0.15, -0.25 + 0.26); t.scale = (1.6, 0.3, 0.5); t.data.materials.append(bord)
    bv = t.modifiers.new('b', 'BEVEL'); bv.width = 0.002; bv.segments = 3
    vm, vnt, vb = L['nmat']('vaggmat')
    vagg = L['plan']('vagg', 6, (0, 0, -0.75), (0, 0, 0), r, vm)
    x0, y0 = L['bild_till_mark'](0.53, 0.0, 'vagg'); x1, y1 = L['bild_till_mark'](0.47, 0.6, 'vagg')
    k = (x0 - x1) / (y0 - y1)  # linje x = x0 + k*(y - y0)
    tc = vnt.nodes.new('ShaderNodeTexCoord'); sp = vnt.nodes.new('ShaderNodeSeparateXYZ'); vnt.links.new(tc.outputs['Object'], sp.inputs[0])
    m1 = vnt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY_ADD'; m1.inputs[1].default_value = -k; m1.inputs[2].default_value = -(x0 - k * y0)
    vnt.links.new(sp.outputs['Y'], m1.inputs[0])
    ad = vnt.nodes.new('ShaderNodeMath'); ad.operation = 'ADD'; vnt.links.new(sp.outputs['X'], ad.inputs[0]); vnt.links.new(m1.outputs[0], ad.inputs[1])
    col = L['ramp'](vnt, ad.outputs[0], [(-0.6, (0.75, 0.75, 0.76)), (-0.01, (0.6, 0.6, 0.61)), (0.01, (0.11, 0.11, 0.115)), (0.6, (0.06, 0.06, 0.065))])
    vnt.links.new(col, vb.inputs['Base Color']); vb.inputs['Roughness'].default_value = 0.9
    # räfflad panel (frostat glas) och stenplatta
    glas = L['mat_enkel']((0.75, 0.76, 0.78), 0.25); glas.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value = 0.6
    for i in range(34):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0042, depth=0.26, vertices=24); c = bpy.context.object; bpy.ops.object.shade_smooth()
        c.parent = r; c.rotation_euler = (math.radians(90), 0, 0); c.location = (-0.035 + i * 0.0085, -0.0828 + 0.13, -0.16); c.data.materials.append(glas)
    sten = L['mat_enkel']((0.09, 0.09, 0.095), 0.9)
    bpy.ops.mesh.primitive_cube_add(size=1); st = bpy.context.object; st.parent = r
    st.location = (0.21, -0.0828 + 0.11, -0.12); st.scale = (0.15, 0.22, 0.025); st.data.materials.append(sten)
    sub = st.modifiers.new('s', 'SUBSURF'); sub.levels = 4; sub.render_levels = 5; sub.subdivision_type = 'SIMPLE'
    tx = bpy.data.textures.new('stenbrus', 'CLOUDS'); tx.noise_scale = 0.03; tx.noise_depth = 6
    dp = st.modifiers.new('d', 'DISPLACE'); dp.texture = tx; dp.strength = 0.016
    sol(r)
else:
    farg, p = P[DEL]
    r = L['star'](farg, p, W, H, ljus=[('fyll', (0.3, 0.1, 0.6), 2.5, 1.5), ('kant', (0.45, 0.25, -0.1), 3, 0.4)], amb=0.0)
    sol(r)
