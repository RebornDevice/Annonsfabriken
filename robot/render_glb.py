"""Renderar produktbilder (genomskinlig bakgrund) från en GLB- eller .blend-fil.
Körs med:  python render_glb.py <fil.glb|fil.blend> <utmapp> [namn]
Ger en PNG per vinkel, beskuren tätt runt produkten.
"""
import sys, os, math
import bpy
from mathutils import Vector

src, outdir = sys.argv[1], sys.argv[2]
name = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(os.path.basename(src))[0]
os.makedirs(outdir, exist_ok=True)

# --- Ladda modellen ---
if src.lower().endswith('.blend'):
    bpy.ops.wm.open_mainfile(filepath=src)
    # ta bort befintliga kameror och lampor så vi får samma ljus överallt
    for o in list(bpy.data.objects):
        if o.type in ('CAMERA', 'LIGHT'):
            bpy.data.objects.remove(o, do_unlink=True)
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)

scene = bpy.context.scene
meshes = [o for o in scene.objects if o.type == 'MESH' and o.visible_get()]
if not meshes:
    raise SystemExit('Hittade ingen modell i filen')

# --- Samla allt under en "rot" och centrera ---
root = bpy.data.objects.new('ProduktRot', None)
scene.collection.objects.link(root)
tops = [o for o in scene.objects if o.parent is None and o is not root and o.type not in ('CAMERA', 'LIGHT')]
for o in tops:
    mw = o.matrix_world.copy(); o.parent = root; o.matrix_world = mw

def bounds():
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx

mn, mx = bounds()
center = (mn + mx) / 2
root.location -= center
size = max((mx - mn))

# --- Ljus: mjukt studioljus ---
def area(name, loc, energy, sz):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy * size * size * 40; l.size = sz * size
    o = bpy.data.objects.new(name, l); scene.collection.objects.link(o); o.location = Vector(loc) * size
    d = -o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('Nyckel', (1.6, -2.2, 1.8), 12, 2.5)
area('Fyll', (-2.2, -1.4, 0.6), 5, 3.0)
area('Kant', (0.0, 2.4, 2.0), 9, 1.5)
area('Topp', (0.0, 0.0, 3.0), 4, 3.0)

world = bpy.data.worlds.new('Studio'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background'); bg.inputs[0].default_value = (0.9, 0.9, 0.92, 1); bg.inputs[1].default_value = 0.35

# --- Rendering ---
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = int(os.environ.get('SAMPLES', '96'))
scene.cycles.use_denoising = True
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.resolution_x = 1600
scene.render.resolution_y = 1600
scene.view_settings.view_transform = 'AgX' if 'AgX' in [v.identifier for v in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'

cam_data = bpy.data.cameras.new('Kamera'); cam_data.lens = 85
cam = bpy.data.objects.new('Kamera', cam_data); scene.collection.objects.link(cam); scene.camera = cam

# Vinklar: (namn, azimut i grader, höjd i grader). Skalets baksida antas peka mot -Y eller +Y; vi testar båda och väljer via env.
facing = float(os.environ.get('FACING', '0'))  # vrid modellen om baksidan pekar åt fel håll
root.rotation_euler[2] = math.radians(facing)
views = [
    ('rakt', 0, 0), ('snett-vanster', -28, 8), ('snett-hoger', 28, 8),
    ('ovanifran', 0, 55), ('lutad', -15, 22), ('profil', -70, 5),
]
dist = size * 4.2
for vname, az, el in views:
    a, e = math.radians(az), math.radians(el)
    cam.location = Vector((dist * math.sin(a) * math.cos(e), -dist * math.cos(a) * math.cos(e), dist * math.sin(e)))
    cam.rotation_euler = (-cam.location).to_track_quat('-Z', 'Y').to_euler()
    path = os.path.join(outdir, f'{name}-{vname}.png')
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print('RENDERAD', path, flush=True)
