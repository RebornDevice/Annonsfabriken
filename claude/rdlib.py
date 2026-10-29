# Hjälpfunktioner för att bygga Reborn-scener i användarens Blender (körs via exec i Blender).
import bpy, math, mathutils
B = '/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/'
G = {'__name__': 'rd'}; exec(open(B + 'Chat Robotfiler/_system/render.py').read(), G)
M = B + 'Chat Material/3D Modeller/18 Pro Max/'
GLB = {'black': M + 'BLACK CASE/Black - 18 Pro Max.glb', 'white': M + 'WHITE CASE/Glacier - 18 Pro Max.glb',
       'blue': M + 'BLUE CASE/Silver - 18 Pro Max.glb', 'orange': M + 'BLACK CASE/Orange - 18 Pro Max.glb'}
UT = B + 'Chat Robotfiler/_system/blender/'

def ny_scen(W, H):
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for c in list(bpy.data.collections): bpy.data.collections.remove(c)
    for blk in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.images, bpy.data.worlds):
        for x in list(blk):
            if x.users == 0: blk.remove(x)
    s = bpy.context.scene; s.render.resolution_x = W; s.render.resolution_y = H; s.render.resolution_percentage = 100
    s.render.engine = 'CYCLES'; s.cycles.device = 'GPU'; s.cycles.use_denoising = True
    s.view_settings.view_transform = 'AgX'; s.view_settings.look = 'AgX - Medium High Contrast'; s.view_settings.exposure = 0

def telefon(farg, p, x=0.0):
    rx, ry, rz = p[0], p[1], p[2]
    return G['importera'](GLB[farg], loc=(x, 0, 0), rot=(90 + rx, ry, rz))

def kamera(p, W, H):
    s = bpy.context.scene
    c = bpy.data.cameras.new('cam'); c.sensor_fit = 'VERTICAL' if H >= W else 'HORIZONTAL'; c.sensor_height = 36; c.sensor_width = 36
    c.lens = p[3]; c.shift_x = p[4]; c.shift_y = p[5]
    o = bpy.data.objects.new('cam', c); s.collection.objects.link(o); s.camera = o
    o.location = (0, -1.0, 0); o.rotation_euler = (math.radians(90), 0, 0); return o

def ljus(namn, loc, mal, e, size, farg=(1, 1, 1)):
    L = bpy.data.lights.new(namn, 'AREA'); L.energy = e; L.size = size; L.color = farg
    o = bpy.data.objects.new(namn, L); bpy.context.scene.collection.objects.link(o); o.location = loc; G['look'](o, mal); return o

def gradient(topp, botten, amb=0.25):
    s = bpy.context.scene; w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True; nt = w.node_tree
    bg = nt.nodes['Background']; tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*botten, 1); ramp.color_ramp.elements[1].color = (*topp, 1)
    nt.links.new(tc.outputs['Window'], sep.inputs[0]); nt.links.new(sep.outputs['Y'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], bg.inputs['Color'])
    lp = nt.nodes.new('ShaderNodeLightPath'); mix = nt.nodes.new('ShaderNodeMixShader'); a = nt.nodes.new('ShaderNodeBackground')
    a.inputs['Color'].default_value = (0.6, 0.62, 0.66, 1); a.inputs['Strength'].default_value = amb
    out = nt.nodes['World Output']; nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs['Fac']); nt.links.new(a.outputs[0], mix.inputs[1])
    nt.links.new(bg.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs['Surface'])

def material_fix():
    G['visa_monster'](2.2); G['skala_uv'](1.15); G['realistiska_linser'](1); G['fixa_kamera'](-1)

def standardljus(e=1.0):
    ljus('nyckel', (-0.5, -0.6, 0.6), (0, 0, 0), 16 * e, 0.8); ljus('kant', (0.5, 0.3, 0.4), (0, 0, 0), 12 * e, 0.4)
    ljus('fyll', (0.3, -0.8, -0.2), (0, 0, 0), 4 * e, 1.2)

def rendera(namn, samples=24, pct=50, transparent=True, mapp=None):
    s = bpy.context.scene; s.cycles.samples = samples; s.render.resolution_percentage = pct
    s.render.film_transparent = transparent; s.render.image_settings.color_mode = 'RGBA' if transparent else 'RGB'
    s.render.filepath = (mapp or UT) + namn + '.png'; bpy.ops.render.render(write_still=True)

def prov(namn, delar, W, H):
    ny_scen(W, H)
    for farg, p in delar: telefon(farg, p)
    material_fix(); kamera(delar[0][1], W, H); standardljus(); gradient((0.3, 0.3, 0.32), (0.3, 0.3, 0.32))
    rendera(namn)
