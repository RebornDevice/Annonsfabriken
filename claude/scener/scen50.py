# Ref 50: en stående och en liggande telefon på salviagrön bakgrund, hårt fönsterljus.
# DEL='bg' (golv+vägg från stående kamerans vy, utan telefoner), '50_0' (stående), '50_1' (liggande)
import bpy, math, mathutils
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
P = {'50_0': (globals().get('F0', 'black'), [5.4179, -4.9324, 38.8996, 137.9866, -0.045384, 0.019827]),
     '50_1': (globals().get('F1', 'blue'), globals().get('P1', [0, 0, 0, 100, 0, 0]))}
W = H = 1080
def sol():
    s = bpy.data.lights.new('sol', 'SUN'); s.energy = 4.5; s.angle = math.radians(2); s.color = (1, 0.95, 0.88)
    o = bpy.data.objects.new('sol', s); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = mathutils.Vector((-0.75, 0.6, -0.55)).to_track_quat('-Z', 'Y').to_euler()
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.75, 0.8, 0.72, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
salvia = (0.22, 0.26, 0.2)
if DEL == 'bg':
    farg, p = P['50_0']
    L['ny_scen'](W, H); r = L['telefon'](farg, p); L['kamera'](p, W, H)
    for o in list(bpy.data.objects):
        if o.type == 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    m = L['mat_enkel'](salvia, 0.85)
    g = L['plan']('golv', 4, (0, -0.0828, 0), (-90, 0, 0), r, m)
    L['plan']('vagg', 6, (0, 0, -1.1), (0, 0, 0), r, m)
    # fönsterkarm utanför bild som ger diagonala skuggor på väggen
    for i in range(3):
        bpy.ops.mesh.primitive_cube_add(size=1); k = bpy.context.object; k.parent = r
        k.location = (0.75, 0.55 + i * 0.3, -0.75); k.scale = (0.5, 0.1, 0.5); k.rotation_euler = (0, 0, 0.7); k.visible_camera = False
    sol()
else:
    farg, p = P[DEL]
    r = L['star'](farg, p, W, H, ljus=[('fyll', (0.2, 0.1, 0.6), 2.0, 1.5)], amb=0.0)
    if DEL == '50_1':  # liggande: golvet är skärmens plan
        g = bpy.data.objects['golv']; g.location = (0, 0, -0.0003); g.rotation_euler = (0, 0, 0)
    sol()
