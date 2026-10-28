# Renderar Reborn-skalet ur GLB i Blender med en bestämd kameravinkel (för att matcha en referens).
# python3 render.py <shot> <ut.png> [glb ...] [--preview]
import bpy, sys, math, mathutils, json

def nolla():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def importera(glb, loc=(0, 0, 0), rot=(0, 0, 0)):
    fore = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=glb)
    nya = [o for o in bpy.data.objects if o not in fore]
    rot_e = bpy.data.objects.new('ROOT_' + glb, None); bpy.context.scene.collection.objects.link(rot_e)
    for o in nya:
        if o.parent is None: o.parent = rot_e
    rot_e.rotation_euler = [math.radians(a) for a in rot]; rot_e.location = loc
    return rot_e

def look(obj, target):
    d = mathutils.Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def kamera(loc, target, lens, W, H, roll=0):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_fit = 'AUTO'
    o = bpy.data.objects.new('cam', c); bpy.context.scene.collection.objects.link(o)
    o.location = loc; look(o, target); o.rotation_euler.rotate_axis('Z', math.radians(roll))
    s = bpy.context.scene; s.camera = o; s.render.resolution_x = W; s.render.resolution_y = H
    c.dof.use_dof = False
    return o

def ljus(namn, loc, target, energi, storlek, farg=(1, 1, 1)):
    l = bpy.data.lights.new(namn, 'AREA'); l.energy = energi; l.size = storlek; l.color = farg
    o = bpy.data.objects.new(namn, l); bpy.context.scene.collection.objects.link(o); o.location = loc; look(o, target)

def golv(z=0, catcher=True, farg=(0.05, 0.05, 0.05)):
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, z)); p = bpy.context.object
    if catcher: p.is_shadow_catcher = True
    m = bpy.data.materials.new('golv'); m.use_nodes = True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*farg, 1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.6
    p.data.materials.append(m); return p

def bakgrund(topp, botten, styrka=1.0):
    # gradientvärld (syns om film inte är transparent)
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree
    bg = nt.nodes['Background']; tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (*botten, 1); ramp.color_ramp.elements[1].color = (*topp, 1)
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -0.4; mr.inputs['From Max'].default_value = 0.6
    nt.links.new(tc.outputs['Window'], sep.inputs[0]); nt.links.new(sep.outputs['Y'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = styrka

def miljoljus(styrka=0.25):
    if not bpy.context.scene.world:
        w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    bpy.context.scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
    bpy.context.scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = styrka

def rendera(ut, transparent=True, samples=64):
    s = bpy.context.scene; s.render.engine = 'CYCLES'; s.cycles.device = 'CPU'
    s.cycles.samples = samples; s.cycles.use_denoising = True; s.render.film_transparent = transparent
    s.view_settings.view_transform = 'AgX'; s.view_settings.look = 'AgX - Medium High Contrast'
    s.render.image_settings.file_format = 'PNG'; s.render.image_settings.color_mode = 'RGBA'
    s.render.filepath = ut; bpy.ops.render.render(write_still=True)

L = 0.165  # telefonens längd (m)
SHOTS = {}
def shot(f): SHOTS[f.__name__] = f; return f

@shot
def nudient_slice(glbs, W, H):  # ref 6: ligger platt på ett stenblock, låg kameravinkel framifrån, kameran till vänster
    importera(glbs[0], loc=(0.07, 0, 0), rot=(0, 0, 90))
    golv(0)
    kamera((0.02, -0.30, 0.12), (0.02, 0.0, 0.0), 58, W, H)
    ljus('topp', (0, 0.05, 0.5), (0, 0, 0), 60, 0.5); ljus('kant', (0.1, 0.4, 0.15), (0, 0, 0), 25, 0.3); ljus('fyll', (-0.3, -0.3, 0.2), (0, 0, 0), 6, 0.6)
    miljoljus(0.15)

@shot
def mous_side(glbs, W, H):  # ref 13: två telefoner stående, sidan mot kameran
    importera(glbs[0], loc=(-0.032, 0, 0.0), rot=(90, 0, -72))
    importera(glbs[1] if len(glbs) > 1 else glbs[0], loc=(0.04, 0.03, 0.0), rot=(90, 0, -72))
    kamera((0.0, -0.40, 0.07), (0.004, 0, 0.065), 70, W, H)
    ljus('kant_v', (-0.25, 0.25, 0.25), (0, 0, 0.08), 40, 0.4); ljus('kant_h', (0.25, 0.25, 0.25), (0, 0, 0.08), 40, 0.4)
    ljus('fyll', (0, -0.4, 0.2), (0, 0, 0.08), 8, 1.0)
    bakgrund((0.035, 0.035, 0.038), (0.008, 0.008, 0.009)); return False

@shot
def nudient_close(glbs, W, H):  # ref 20: närbild diagonalt, kameramodulen uppe till vänster
    importera(glbs[0], loc=(0, 0, 0), rot=(20, 0, -40))
    kamera((0.0, -0.06, 0.16), (0.012, 0.012, 0.0), 45, W, H)
    ljus('topp', (0, 0.2, 0.35), (0, 0, 0), 30, 0.5); ljus('sida', (-0.3, 0, 0.1), (0, 0, 0), 10, 0.5)
    bakgrund((0.05, 0.05, 0.06), (0.75, 0.77, 0.8)); return False

@shot
def nudient_grus(glbs, W, H):  # ref 29: ligger platt diagonalt, sett snett ovanifrån, liten i bild
    importera(glbs[0], loc=(0, 0, 0), rot=(0, 0, -62))
    golv(0)
    kamera((0.0, -0.36, 0.42), (0.0, 0.07, 0.0), 55, W, H)
    ljus('topp', (-0.2, 0.2, 0.6), (0, 0, 0), 40, 0.8); ljus('fyll', (0.3, -0.3, 0.3), (0, 0, 0), 8, 0.8)
    miljoljus(0.15)

@shot
def peel_podium(glbs, W, H):  # ref 56: står upp, 3/4-vinkel, sett lite underifrån
    importera(glbs[0], loc=(0, 0, 0.0827), rot=(90, 0, 38))
    golv(0)
    kamera((0.06, -0.40, 0.05), (-0.075, 0, 0.15), 50, W, H)
    ljus('kant', (0.25, 0.2, 0.3), (0, 0, 0.08), 35, 0.4); ljus('fyll', (-0.2, -0.3, 0.2), (0, 0, 0.08), 10, 0.8)
    miljoljus(0.15)

@shot
def bullstrap_stand(glbs, W, H):  # ref 18: står upp, baksidan mot kameran, nära, något vriden
    importera(glbs[0], loc=(0, 0, 0.0827), rot=(90, 0, 15))
    golv(0)
    kamera((-0.03, -0.30, 0.05), (-0.03, 0, 0.11), 50, W, H)
    ljus('nyckel', (-0.3, -0.2, 0.3), (0, 0, 0.08), 30, 0.8); ljus('kant', (0.3, 0.2, 0.2), (0, 0, 0.08), 15, 0.4)
    miljoljus(0.3)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    prev = '--preview' in sys.argv
    namn, ut, glbs = a[0], a[1], a[2:]
    W, H = (270, 480) if prev else (1080, 1920)
    nolla(); r = SHOTS[namn](glbs, W, H)
    rendera(ut, transparent=(r is not False), samples=8 if prev else 48)
