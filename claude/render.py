# Renderar Reborn-skalet ur GLB i Blender med en bestämd kameravinkel (för att matcha en referens).
# python3 render.py <shot> <ut.png> [glb ...] [--preview]
import bpy, sys, math, mathutils, json, os
PROXY = os.environ.get('PROXY') == '1'  # grå platshållare (block/podium/bord) som ChatGPT målar om

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
    l = bpy.data.lights.new(namn, 'AREA'); l.energy = energi * LJUSFAKTOR; l.size = storlek; l.color = farg
    o = bpy.data.objects.new(namn, l); bpy.context.scene.collection.objects.link(o); o.location = loc; look(o, target)

def golv(z=0, catcher=True, farg=(0.05, 0.05, 0.05)):
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, z)); p = bpy.context.object
    if catcher: p.is_shadow_catcher = True
    m = bpy.data.materials.new('golv'); m.use_nodes = True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*farg, 1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.6
    p.data.materials.append(m); return p

def visa_monster(styrka=1.0):
    # Gör aramidvävens mönster tydligare: djupare struktur, lite blankare yta, mer kontrast i färgen
    for m in bpy.data.materials:
        if not m.use_nodes or 'aramid' not in m.name.lower(): continue
        nt = m.node_tree; b = nt.nodes['Principled BSDF']
        for n in nt.nodes:
            if n.type == 'NORMAL_MAP': n.inputs['Strength'].default_value = 1.0 + 1.0 * styrka
        tex = [n for n in nt.nodes if n.type == 'TEX_IMAGE' and b.inputs['Base Color'].links and b.inputs['Base Color'].links[0].from_node == n]
        if tex:
            # mer kontrast: de grå ränderna blir ljusare, det svarta förblir nästan svart
            k = 1 + 0.8 * styrka; vm = nt.nodes.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY_ADD'  # linjära värden: svart ~0.003, rand ~0.02
            vm.inputs[1].default_value = (k, k, k); vm.inputs[2].default_value = (0.002,) * 3
            mx = nt.nodes.new('ShaderNodeVectorMath'); mx.operation = 'MAXIMUM'; mx.inputs[1].default_value = (0.0, 0.0, 0.0)
            nt.links.new(tex[0].outputs['Color'], vm.inputs[0]); nt.links.new(vm.outputs['Vector'], mx.inputs[0]); nt.links.new(mx.outputs['Vector'], b.inputs['Base Color'])

def skala_uv(k):
    # ändrar storleken på vävmönstret (k > 1 = mindre/tätare mönster)
    for m in bpy.data.materials:
        if not m.use_nodes or 'aramid' not in m.name.lower(): continue
        nt = m.node_tree; tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (k, k, 1); nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])
        for n in nt.nodes:
            if n.type == 'TEX_IMAGE': nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])

def fixa_kamera(glans=1.0):
    # Ljus silverram och blanka linser som på riktiga foton
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        b = m.node_tree.nodes.get('Principled BSDF')
        if not b: continue
        n = m.name.lower()
        if 'titanium' in n and 'inside' not in n:   # bara kameraramen och knapparna: satinerad aluminium med skiftande glans
            nt = m.node_tree; lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35
            rmp = nt.nodes.new('ShaderNodeValToRGB'); rmp.color_ramp.elements[0].color = (0.75, 0.76, 0.78, 1); rmp.color_ramp.elements[1].color = (0.16, 0.165, 0.17, 1)
            nt.links.new(lw.outputs['Facing'], rmp.inputs['Fac']); nt.links.new(rmp.outputs['Color'], b.inputs['Base Color'])
            b.inputs['Metallic'].default_value = 0.5; b.inputs['Roughness'].default_value = 0.16
    if glans < 0: return   # bara ramen/knapparna ändras, inga extra reflexer
    if glans == 0: return
    # reflexer: världen syns ljusare bara i speglingar (påverkar inte hur ljus skalet blir)
    w = bpy.context.scene.world
    if not w:
        w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    nt = w.node_tree; out = nt.nodes['World Output']; gammal = out.inputs['Surface'].links[0].from_socket if out.inputs['Surface'].links else None
    lp = nt.nodes.new('ShaderNodeLightPath'); bg2 = nt.nodes.new('ShaderNodeBackground'); bg2.inputs['Strength'].default_value = glans
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = -0.2; mr.inputs['From Max'].default_value = 1.0
    nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], bg2.inputs['Color'])
    mix = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(lp.outputs['Is Glossy Ray'], mix.inputs['Fac'])
    if gammal: nt.links.new(gammal, mix.inputs[1])
    else:
        bg0 = nt.nodes.new('ShaderNodeBackground'); bg0.inputs['Strength'].default_value = 0; nt.links.new(bg0.outputs[0], mix.inputs[1])
    nt.links.new(bg2.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs['Surface'])

def metall_reflexer(styrka=1.0):
    for m in bpy.data.materials:
        if m.use_nodes and 'titanium' in m.name.lower():
            bb = m.node_tree.nodes['Principled BSDF']
            if 'inside' in m.name.lower():   # plattan inuti ramen ska vara mörk som på riktiga telefonen
                bb.inputs['Base Color'].default_value = (0.025, 0.025, 0.027, 1); bb.inputs['Metallic'].default_value = 0.0
                bb.inputs['Roughness'].default_value = 0.6; bb.inputs['Specular IOR Level'].default_value = 0.0; continue
            bb.inputs['Base Color'].default_value = (0.8, 0.81, 0.83, 1); bb.inputs['Metallic'].default_value = 1.0
            bb.inputs['Roughness'].default_value = 0.22
    kol = bpy.data.collections.new('metall'); bpy.context.scene.collection.children.link(kol)
    for o in bpy.data.objects:
        if o.type == 'MESH' and 'lip' not in o.name.lower() and any(mm and 'titanium' in mm.name.lower() for mm in o.data.materials): kol.objects.link(o)
    cam = bpy.context.scene.camera.location
    for namn, loc, e, sx, sy in [('list_bak', (cam.x + 0.02, 0.28, 0.2), 6, 0.6, 0.06), ('list_fram', (cam.x, cam.y - 0.2, 0.25), 3, 0.5, 0.08),
                                 ('list_sida', (0.45, -0.05, 0.12), 3, 0.08, 0.4)]:
        l = bpy.data.lights.new(namn, 'AREA'); l.shape = 'RECTANGLE'; l.size = sx; l.size_y = sy; l.energy = e * styrka * LJUSFAKTOR * 10
        o = bpy.data.objects.new(namn, l); bpy.context.scene.collection.objects.link(o); o.location = loc; look(o, (0.05, 0, 0.005))
        o.light_linking.receiver_collection = kol

def lada(namn, loc, storlek, farg, rough=0.8):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = namn; o.scale = storlek
    m = bpy.data.materials.new(namn); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*farg, 1); b.inputs['Roughness'].default_value = rough; o.data.materials.append(m); return o

def cylinder(namn, loc, r, h, farg, rough=0.3):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc, vertices=96); o = bpy.context.object
    bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new(namn); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*farg, 1); b.inputs['Roughness'].default_value = rough; o.data.materials.append(m); return o

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
LJUSFAKTOR = 0.3
SHOTS = {}
def shot(f): SHOTS[f.__name__] = f; return f

@shot
def nudient_slice(glbs, W, H):  # ref 6: ligger platt på ett stenblock, låg kameravinkel framifrån, kameran till vänster
    importera(glbs[0], loc=(0.07, 0, 0), rot=(0, 0, 90))
    if PROXY:
        lada('block', (0.12, 0.08, -0.15), (0.34, 0.2, 0.3), (0.06, 0.06, 0.065)); bakgrund((0.02, 0.02, 0.022), (0.05, 0.05, 0.055))
        ljus('topp', (0, 0.05, 0.5), (0, 0, 0), 60, 0.5); ljus('kant', (0.1, 0.4, 0.15), (0, 0, 0), 25, 0.3); ljus('fyll', (-0.3, -0.3, 0.2), (0, 0, 0), 6, 0.6)
        kamera((0.02, -0.30, 0.12), (0.02, 0.0, 0.0), 58, W, H); return False
    golv(0)
    kamera((0.02, -0.30, 0.12), (0.02, 0.0, 0.0), 58, W, H)
    ljus('topp', (0, 0.05, 0.5), (0, 0, 0), 60, 0.5); ljus('kant', (0.1, 0.4, 0.15), (0, 0, 0), 25, 0.3); ljus('fyll', (-0.3, -0.3, 0.2), (0, 0, 0), 6, 0.6)
    miljoljus(0.15)

@shot
def nudient_slice2(glbs, W, H):  # ref 6 v2: stort stenblock, låg kamera, mjukt ljus, telefonen stor och beskuren till höger
    P = {'phone': [0.075, 0.0, 0.0], 'cam': [0.03, -0.24, 0.055], 'tgt': [0.045, 0.0, 0.004], 'lens': 52,
         'block': [0.17, 0.19, -0.3, 0.5, 0.42, 0.6], 'topp': 6, 'kant': 10, 'fyll': 1.2}
    P.update(json.loads(os.environ.get('SHOT', '{}')))
    importera(glbs[0], loc=tuple(P['phone']), rot=(0, 0, P.get('rotz', 90)))
    if P.get('monster'): visa_monster(P['monster'])
    if P.get('uv'): skala_uv(P['uv'])
    kamera(tuple(P['cam']), tuple(P['tgt']), P['lens'], W, H)
    if P.get('glans'):  # mjuk ljuslåda bakom telefonen: speglas i ovansidan så att vävmönstret syns
        ljus('glans', (P['phone'][0], 0.30, 0.07), (P['phone'][0], 0, 0.008), P['glans'], 0.5)
    # mjukt stort ljus ovanifrån-bakifrån (ger kantljus), svag fyllning framifrån
    ljus('topp', tuple(P.get('topp_pos', (0.05, 0.25, 0.45))), (0.05, 0, 0), P['topp'], 1.2)
    if P.get('rake'): ljus('rake', (-0.35, 0.0, 0.04), (0.08, 0, 0.005), P['rake'], 0.4)
    ljus('kant', (0.35, 0.3, 0.12), (0.05, 0, 0), P['kant'], 0.6)
    ljus('fyll', (-0.25, -0.35, 0.15), (0.05, 0, 0), P['fyll'], 1.5)
    if PROXY:
        b = P['block']; lada('block', (b[0], b[1], b[2]), (b[3], b[4], b[5]), (0.12, 0.12, 0.125), 0.9)
        bakgrund((0.012, 0.012, 0.014), (0.03, 0.03, 0.034))
        if P.get('kamera'): fixa_kamera(P['kamera'])
        return False
    miljoljus(0.04)
    if P.get('kamera'): fixa_kamera(P['kamera'])

@shot
def topp_test(glbs, W, H):  # ovanifrån som användarens foto, för att jämföra mönstret
    P = {'monster': 0}; P.update(json.loads(os.environ.get('SHOT', '{}')))
    importera(glbs[0], loc=(0, 0, 0), rot=(0, 0, P.get('rotz', 0)))
    if P.get('monster'): visa_monster(P['monster'])
    if P.get('uv'): skala_uv(P['uv'])
    kamera(tuple(P.get('cam', (0.0, -0.05, 0.42))), tuple(P.get('tgt', (0, 0.0, 0))), P.get('lens', 50), W, H)
    ljus('topp', (0.0, 0.3, 0.6), (0, 0, 0), 25, 1.0); ljus('fyll', (0, -0.3, 0.5), (0, 0, 0), 6, 1.2)
    golv(0, catcher=False, farg=(0.04, 0.04, 0.045)); miljoljus(0.05)
    if P.get('kamera'): fixa_kamera(P['kamera'])
    return False

@shot
def mous_side(glbs, W, H):  # ref 13: två telefoner stående, sidan mot kameran
    importera(glbs[0], loc=(-0.026, 0, 0.0), rot=(90, 0, -78))
    importera(glbs[1] if len(glbs) > 1 else glbs[0], loc=(0.03, 0.03, 0.0), rot=(90, 0, -78))
    kamera((0.0, -0.40, 0.06), (0.004, 0, 0.042), 85, W, H)
    ljus('kant_v', (-0.25, 0.25, 0.25), (0, 0, 0.08), 40, 0.4); ljus('kant_h', (0.25, 0.25, 0.25), (0, 0, 0.08), 40, 0.4)
    ljus('fyll', (-0.3, -0.3, -0.1), (0, 0, 0.05), 3, 1.0)
    bakgrund((0.035, 0.035, 0.038), (0.008, 0.008, 0.009)); return False

@shot
def nudient_close(glbs, W, H):  # ref 20: närbild diagonalt, kameramodulen uppe till vänster
    importera(glbs[0], loc=(0, 0, 0), rot=(20, 0, 40))
    kamera((-0.02, -0.035, 0.16), (-0.03, 0.035, 0.0), 45, W, H)
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
    if PROXY:
        cylinder('podium', (0, 0, -0.15), 0.065, 0.3, (0.02, 0.02, 0.022), 0.25)
        lada('vagg', (0, 0.45, 0.2), (2, 0.02, 1.5), (0.18, 0.03, 0.06), 0.6)
        ljus('kant', (0.25, 0.2, 0.3), (0, 0, 0.08), 35, 0.4); ljus('fyll', (-0.2, -0.3, 0.2), (0, 0, 0.08), 10, 0.8); ljus('vagg', (0, 0.1, 0.4), (0, 0.45, 0.2), 40, 1.0)
        kamera((0.06, -0.40, 0.05), (-0.042, 0, 0.125), 50, W, H); miljoljus(0.1); return False
    golv(0)
    kamera((0.06, -0.40, 0.05), (-0.042, 0, 0.125), 50, W, H)
    ljus('kant', (0.25, 0.2, 0.3), (0, 0, 0.08), 35, 0.4); ljus('fyll', (-0.2, -0.3, 0.2), (0, 0, 0.08), 10, 0.8)
    miljoljus(0.15)

@shot
def peel2(glbs, W, H):  # ref 56 v2: står på stort podium, baksida + höger sida, till höger i bild, lite underifrån
    P = {'rotz': -28, 'tilt': 0, 'cam': [0.0, -0.478, 0.03], 'tgt': [-0.046, 0, 0.1375], 'lens': 50,
         'pod_r': 0.09, 'nyckel': 14, 'kant': 18, 'fyll': 5, 'monster': 3.6, 'uv': 1.15, 'kamera': -1}
    P.update(json.loads(os.environ.get('SHOT', '{}')))
    importera(glbs[0], loc=(0, 0, 0.0827), rot=(90 + P['tilt'], 0, P['rotz']))
    if P.get('monster'): visa_monster(P['monster'])
    if P.get('uv'): skala_uv(P['uv'])
    kamera(tuple(P['cam']), tuple(P['tgt']), P['lens'], W, H)
    ljus('nyckel', (-0.3, -0.35, 0.35), (0, 0, 0.08), P['nyckel'], 1.0)
    ljus('kant', (0.3, 0.15, 0.25), (0, 0, 0.08), P['kant'], 0.4)
    ljus('fyll', (0.1, -0.4, 0.05), (0, 0, 0.08), P['fyll'], 1.2)
    if P.get('plommon'): ljus('plommon', (-0.35, -0.1, 0.15), (0, 0, 0.1), P['plommon'], 1.5, (1.0, 0.35, 0.55))
    if P.get('lins'):   # liten ljuskälla som speglas i kameraglaset och linserna
        for m in bpy.data.materials:
            if m.use_nodes and m.name.lower().startswith('base_cam_lens') and 'outer' not in m.name.lower():
                bb = m.node_tree.nodes['Principled BSDF']; bb.inputs['Roughness'].default_value = 0.08; bb.inputs['Coat Weight'].default_value = 1.0
        ljus('lins', tuple(P.get('lins_pos', (-0.15, -0.35, 0.35))), (-0.01, 0, 0.14), P['lins'], 0.15)
    pod = cylinder('podium', (0, 0.02, -0.15), P['pod_r'], 0.3, tuple(P.get('pod_farg', (0.09, 0.025, 0.05))), P.get('pod_rough', 0.3))
    pb = pod.data.materials[0].node_tree.nodes['Principled BSDF']; pb.inputs['Metallic'].default_value = P.get('pod_metal', 0.7)
    bv = pod.modifiers.new('bevel', 'BEVEL'); bv.width = 0.003; bv.segments = 6
    ljus('podkant', (0.0, 0.35, 0.06), (0, 0.02, 0), P.get('podljus', 6), 0.8)
    if PROXY:
        lada('vagg', (0, 0.6, 0.2), (3, 0.02, 2), (0.12, 0.03, 0.06), 0.7)
        ljus('vagg', (0, 0.2, 0.5), (0, 0.6, 0.2), 60, 2.0)
        miljoljus(0.05)
        if P.get('kamera'): fixa_kamera(P['kamera'])
        return False
    miljoljus(0.04)
    if P.get('kamera'): fixa_kamera(P['kamera'])

@shot
def bullstrap_stand(glbs, W, H):  # ref 18: står upp, baksidan mot kameran, nära, något vriden
    importera(glbs[0], loc=(0, 0, 0.0827), rot=(90, 0, 15))
    if PROXY:
        lada('bord', (0, 0.2, -0.01), (2, 1.2, 0.02), (0.45, 0.18, 0.08), 0.5)
        lada('vagg', (0, 0.6, 0.4), (3, 0.02, 1.2), (0.85, 0.83, 0.8), 0.9)
        ljus('nyckel', (-0.3, -0.2, 0.3), (0, 0, 0.08), 30, 0.8); ljus('kant', (0.3, 0.2, 0.2), (0, 0, 0.08), 15, 0.4); ljus('vagg', (-0.2, 0.2, 0.5), (0, 0.6, 0.3), 60, 1.5)
        kamera((-0.03, -0.45, 0.06), (-0.04, 0, 0.1), 62, W, H); miljoljus(0.4); return False
    golv(0)
    kamera((-0.03, -0.45, 0.06), (-0.04, 0, 0.1), 62, W, H)
    ljus('nyckel', (-0.3, -0.2, 0.3), (0, 0, 0.08), 30, 0.8); ljus('kant', (0.3, 0.2, 0.2), (0, 0, 0.08), 15, 0.4)
    miljoljus(0.3)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    prev = '--preview' in sys.argv
    namn, ut, glbs = a[0], a[1], a[2:]
    mid = '--mid' in sys.argv
    W, H = (270, 480) if prev else ((540, 960) if mid else (1080, 1920))
    nolla(); r = SHOTS[namn](glbs, W, H)
    rendera(ut, transparent=(r is not False), samples=8 if prev else (24 if mid else (16 if PROXY else 48)))
