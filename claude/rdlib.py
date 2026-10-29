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

# ---------- Hela scener (mark/golv/vägg) som följer telefonens rotation ----------
# Telefonens lokala koordinater: x bredd (±0.041), y längd (±0.083, kamera uppåt +y), z 0 = skärm, 0.0112 = baksida
def plan(namn, storlek, loc, rot, foralder, mat):
    import bmesh
    me = bpy.data.meshes.new(namn); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=storlek / 2)
    for f in bm.faces: f.smooth = True
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(namn, me); bpy.context.scene.collection.objects.link(o)
    o.parent = foralder; o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]
    uv = me.uv_layers.new(); o.data.materials.append(mat); return o

def nmat(namn):
    m = bpy.data.materials.new(namn); m.use_nodes = True; nt = m.node_tree; return m, nt, nt.nodes['Principled BSDF']

def koord(nt, skala=1.0):
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (skala,) * 3
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); return mp.outputs['Vector']

def ramp(nt, fac, stopp):
    r = nt.nodes.new('ShaderNodeValToRGB'); e = r.color_ramp.elements
    e[0].position, e[0].color = stopp[0][0], (*stopp[0][1], 1); e[1].position, e[1].color = stopp[-1][0], (*stopp[-1][1], 1)
    for p, c in stopp[1:-1]: n = e.new(p); n.color = (*c, 1)
    nt.links.new(fac, r.inputs['Fac']); return r.outputs['Color']

def bump(nt, b, h, styrka, dist=0.002):
    bu = nt.nodes.new('ShaderNodeBump'); bu.inputs['Strength'].default_value = styrka; bu.inputs['Distance'].default_value = dist
    nt.links.new(h, bu.inputs['Height']); nt.links.new(bu.outputs['Normal'], b.inputs['Normal'])

def mat_asfalt(ljus=0.012, flack=0.5, skala=300):
    # svart sand/asfalt med små ljusa korn
    m, nt, b = nmat('asfalt'); v = koord(nt)
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 2500; n1.inputs['Detail'].default_value = 1
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 20; n2.inputs['Detail'].default_value = 6
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = skala
    for n in (n1, n2, vo): nt.links.new(v, n.inputs['Vector'])
    prick = ramp(nt, vo.outputs['Distance'], [(0.0, (1, 1, 1)), (0.06, (1, 1, 1)), (0.13, (0, 0, 0))])
    sc = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(vo.outputs['Color'], sc.inputs[0])
    styrka = ramp(nt, sc.outputs[0], [(0.0, (0, 0, 0)), (1 - flack, (0, 0, 0)), (1.0, (1, 1, 1))])
    mp = nt.nodes.new('ShaderNodeMix'); mp.data_type = 'RGBA'; mp.blend_type = 'MULTIPLY'; mp.inputs['Factor'].default_value = 1
    nt.links.new(prick, mp.inputs['A']); nt.links.new(styrka, mp.inputs['B'])
    sp = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(mp.outputs['Result'], sp.inputs[0])
    korn = ramp(nt, n1.outputs['Fac'], [(0.3, (ljus * .5,) * 3), (0.7, (ljus * 1.6,) * 3)])
    stor = ramp(nt, n2.outputs['Fac'], [(0.3, (0.7,) * 3), (0.7, (1.2,) * 3)])
    mk = nt.nodes.new('ShaderNodeMix'); mk.data_type = 'RGBA'; mk.blend_type = 'MULTIPLY'; mk.inputs['Factor'].default_value = 1
    nt.links.new(korn, mk.inputs['A']); nt.links.new(stor, mk.inputs['B'])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['B'].default_value = (0.35, 0.34, 0.33, 1)
    nt.links.new(sp.outputs[0], mx.inputs['Factor']); nt.links.new(mk.outputs['Result'], mx.inputs['A']); nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    rr = ramp(nt, sp.outputs[0], [(0.0, (0.75,) * 3), (1.0, (0.3,) * 3)]); nt.links.new(rr, b.inputs['Roughness'])
    bump(nt, b, n1.outputs['Fac'], 0.5, 0.0008); return m

def mat_sand(bas=0.002, lager=((650, 0.45, 3.0), (1500, 0.18, 2.0), (3000, 0.06, 1.0)), tint=(1.0, 0.97, 0.94)):
    # svart sand: flera lager korn med olika storlek och ljushet
    m, nt, b = nmat('sand'); v = koord(nt); farg = None; hojd = None
    for skala, ljus, pot in lager:
        vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = skala; nt.links.new(v, vo.inputs['Vector'])
        dot = ramp(nt, vo.outputs['Distance'], [(0.0, (1, 1, 1)), (0.22, (0.8, 0.8, 0.8)), (0.42, (0, 0, 0))])
        sc = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(vo.outputs['Color'], sc.inputs[0])
        pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = pot; nt.links.new(sc.outputs[0], pw.inputs[0])
        sd = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(dot, sd.inputs[0])
        mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; nt.links.new(pw.outputs[0], mu.inputs[0]); nt.links.new(sd.outputs[0], mu.inputs[1])
        mu2 = nt.nodes.new('ShaderNodeMath'); mu2.operation = 'MULTIPLY'; mu2.inputs[1].default_value = ljus; nt.links.new(mu.outputs[0], mu2.inputs[0])
        if farg is None: farg, hojd = mu2.outputs[0], sd.outputs[0]
        else:
            ad = nt.nodes.new('ShaderNodeMath'); ad.operation = 'ADD'; nt.links.new(farg, ad.inputs[0]); nt.links.new(mu2.outputs[0], ad.inputs[1]); farg = ad.outputs[0]
            ah = nt.nodes.new('ShaderNodeMath'); ah.operation = 'MAXIMUM'; nt.links.new(hojd, ah.inputs[0]); nt.links.new(sd.outputs[0], ah.inputs[1]); hojd = ah.outputs[0]
    ab = nt.nodes.new('ShaderNodeMath'); ab.operation = 'ADD'; ab.inputs[1].default_value = bas; nt.links.new(farg, ab.inputs[0])
    cm = nt.nodes.new('ShaderNodeCombineColor'); 
    for i, t in enumerate(tint):
        mt = nt.nodes.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = t; nt.links.new(ab.outputs[0], mt.inputs[0]); nt.links.new(mt.outputs[0], cm.inputs[i])
    nt.links.new(cm.outputs[0], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.55
    bump(nt, b, hojd, 0.8, 0.0008); return m

def mat_lera(mossa=None, skala=40, fin=130, farger=((0.13, 0.028, 0.010), (0.24, 0.055, 0.022), (0.38, 0.12, 0.055))):
    # sprucken röd/orange lera; mossa = (x, y, radie) i markens lokala koordinater
    m, nt, b = nmat('lera'); v = koord(nt)
    wv = nt.nodes.new('ShaderNodeTexNoise'); wv.inputs['Scale'].default_value = 35; wv.inputs['Detail'].default_value = 4
    nt.links.new(v, wv.inputs['Vector'])
    mixv = nt.nodes.new('ShaderNodeMix'); mixv.data_type = 'VECTOR'; mixv.inputs['Factor'].default_value = 0.022
    nt.links.new(v, mixv.inputs['A']); nt.links.new(wv.outputs['Color'], mixv.inputs['B'])
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.feature = 'DISTANCE_TO_EDGE'; vo.inputs['Scale'].default_value = skala
    nt.links.new(mixv.outputs['Result'], vo.inputs['Vector'])
    vo2 = nt.nodes.new('ShaderNodeTexVoronoi'); vo2.feature = 'DISTANCE_TO_EDGE'; vo2.inputs['Scale'].default_value = fin
    nt.links.new(mixv.outputs['Result'], vo2.inputs['Vector'])
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 60; n2.inputs['Detail'].default_value = 8
    nt.links.new(v, n2.inputs['Vector'])
    spr = ramp(nt, vo.outputs['Distance'], [(0.0, (0, 0, 0)), (0.018, (0, 0, 0)), (0.05, (1, 1, 1))])
    spr2 = ramp(nt, vo2.outputs['Distance'], [(0.0, (0.35, 0.35, 0.35)), (0.025, (1, 1, 1))])
    ml = nt.nodes.new('ShaderNodeMix'); ml.data_type = 'RGBA'; ml.blend_type = 'MULTIPLY'; ml.inputs['Factor'].default_value = 1
    nt.links.new(spr, ml.inputs['A']); nt.links.new(spr2, ml.inputs['B'])
    farg = ramp(nt, n2.outputs['Fac'], [(0.3, farger[0]), (0.5, farger[1]), (0.7, farger[2])])
    mc = nt.nodes.new('ShaderNodeMix'); mc.data_type = 'RGBA'; mc.inputs['A'].default_value = (0.012, 0.004, 0.002, 1)
    nt.links.new(ml.outputs['Result'], mc.inputs['Factor']); nt.links.new(farg, mc.inputs['B'])
    ut = mc.outputs['Result']
    if mossa:
        # mossa = lista av (x, y, radie) i markens lokala koordinater
        nm = nt.nodes.new('ShaderNodeTexNoise'); nm.inputs['Scale'].default_value = 45; nm.inputs['Detail'].default_value = 8; nt.links.new(v, nm.inputs['Vector'])
        minst = None
        for (mx_, my_, rr) in mossa:
            dx = nt.nodes.new('ShaderNodeVectorMath'); dx.operation = 'DISTANCE'; dx.inputs[1].default_value = (mx_, my_, 0); nt.links.new(v, dx.inputs[0])
            dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = rr; nt.links.new(dx.outputs['Value'], dv.inputs[0])
            if minst is None: minst = dv.outputs[0]
            else:
                mi = nt.nodes.new('ShaderNodeMath'); mi.operation = 'MINIMUM'; nt.links.new(minst, mi.inputs[0]); nt.links.new(dv.outputs[0], mi.inputs[1]); minst = mi.outputs[0]
        ad = nt.nodes.new('ShaderNodeMath'); ad.operation = 'MULTIPLY_ADD'; ad.inputs[1].default_value = 1.4; nt.links.new(nm.outputs['Fac'], ad.inputs[0]); nt.links.new(minst, ad.inputs[2])
        mk = ramp(nt, ad.outputs[0], [(0.0, (1, 1, 1)), (1.15, (1, 1, 1)), (1.3, (0, 0, 0)), (1.0, (0, 0, 0))]) if False else None
        rmp = nt.nodes.new('ShaderNodeMapRange'); rmp.inputs['From Min'].default_value = 1.35; rmp.inputs['From Max'].default_value = 1.45
        rmp.inputs['To Min'].default_value = 1; rmp.inputs['To Max'].default_value = 0; nt.links.new(ad.outputs[0], rmp.inputs['Value'])
        mkv = rmp.outputs['Result']
        nm2 = nt.nodes.new('ShaderNodeTexNoise'); nm2.inputs['Scale'].default_value = 60; nm2.inputs['Detail'].default_value = 4; nt.links.new(v, nm2.inputs['Vector'])
        nm3 = nt.nodes.new('ShaderNodeTexVoronoi'); nm3.inputs['Scale'].default_value = 280; nt.links.new(v, nm3.inputs['Vector'])
        klump = ramp(nt, nm3.outputs['Distance'], [(0.0, (0.10, 0.17, 0.03)), (0.45, (0.035, 0.075, 0.012)), (0.9, (0.004, 0.01, 0.002))])
        vari = ramp(nt, nm2.outputs['Fac'], [(0.3, (0.55, 0.6, 0.5)), (0.7, (1.3, 1.2, 1.0))])
        gr = nt.nodes.new('ShaderNodeMix'); gr.data_type = 'RGBA'; gr.blend_type = 'MULTIPLY'; gr.inputs['Factor'].default_value = 1
        nt.links.new(klump, gr.inputs['A']); nt.links.new(vari, gr.inputs['B'])
        mm = nt.nodes.new('ShaderNodeMix'); mm.data_type = 'RGBA'; nt.links.new(mkv, mm.inputs['Factor']); nt.links.new(ut, mm.inputs['A']); nt.links.new(gr.outputs['Result'], mm.inputs['B'])
        ut = mm.outputs['Result']
        sepm = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(ml.outputs['Result'], sepm.inputs[0])
        inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; nt.links.new(nm3.outputs['Distance'], inv.inputs[1])
        hm = nt.nodes.new('ShaderNodeMix'); hm.data_type = 'FLOAT'; nt.links.new(mkv, hm.inputs['Factor']); nt.links.new(sepm.outputs[0], hm.inputs['A']); nt.links.new(inv.outputs[0], hm.inputs['B'])
        h = hm.outputs['Result']
    else:
        sepm = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(ml.outputs['Result'], sepm.inputs[0]); h = sepm.outputs[0]
    nt.links.new(ut, b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.9
    bump(nt, b, h, 1.0, 0.0015); return m

def mat_tra(farg=(0.22, 0.08, 0.03)):
    # varm trävägg med lodräta fibrer
    m, nt, b = nmat('tra'); v = koord(nt)
    w = nt.nodes.new('ShaderNodeTexWave'); w.wave_type = 'BANDS'; w.bands_direction = 'X'; w.inputs['Scale'].default_value = 6
    w.inputs['Distortion'].default_value = 6; w.inputs['Detail'].default_value = 6; w.inputs['Detail Scale'].default_value = 1.5
    nt.links.new(v, w.inputs['Vector'])
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 3; nt.links.new(v, n.inputs['Vector'])
    f = [c * k for c in farg for k in (1,)]
    col = ramp(nt, w.outputs['Fac'], [(0.0, tuple(c * 0.55 for c in farg)), (0.5, tuple(farg)), (1.0, tuple(c * 1.45 for c in farg))])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 0.35
    nt.links.new(col, mx.inputs['A']); nt.links.new(n.outputs['Color'], mx.inputs['B']); nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.5; b.inputs['Coat Weight'].default_value = 0.3; bump(nt, b, w.outputs['Fac'], 0.15, 0.001); return m

def mat_enkel(farg, rough=0.5, metal=0.0, coat=0.0):
    m, nt, b = nmat('enkel'); b.inputs['Base Color'].default_value = (*farg, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; b.inputs['Coat Weight'].default_value = coat; return m

def lokalt_ljus(root, namn, lok, e, size, farg=(1, 1, 1), mal=(0, 0, 0.005)):
    L = bpy.data.lights.new(namn, 'AREA'); L.energy = e; L.size = size; L.color = farg
    o = bpy.data.objects.new(namn, L); bpy.context.scene.collection.objects.link(o); o.parent = root; o.location = lok
    d = mathutils.Vector(mal) - mathutils.Vector(lok); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o

def ligger(farg, p, W, H, mark, ljus=None, amb=0.15):
    # telefonen ligger med skärmen ned på en mark (mark = material), allt renderas i Blender
    ny_scen(W, H); r = telefon(farg, p); material_fix(); kamera(p, W, H)
    mark = mark() if callable(mark) else mark
    plan('mark', 3, (0, 0, -0.0003), (0, 0, 0), r, mark)
    for nm, lok, e, s, *f in (ljus or [('nyckel', (-0.35, 0.45, 0.6), 60, 0.35), ('fyll', (0.4, -0.3, 0.5), 8, 1.5)]):
        lokalt_ljus(r, nm, lok, e, s, *(f or [(1, 1, 1)]))
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.6, 0.62, 0.66, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = amb
    return r

def bild_till_mark(u, v, namn='mark'):
    # bildpunkt (u, v), 0..1 från vänster/uppifrån -> markens lokala (x, y)
    sc = bpy.context.scene; cam = sc.camera; bpy.context.view_layer.update()
    fr = cam.data.view_frame(scene=sc)  # [övre höger, nedre höger, nedre vänster, övre vänster]
    tl, tr, bl = fr[3], fr[0], fr[2]
    p = tl + (tr - tl) * u + (bl - tl) * v
    o = cam.matrix_world @ mathutils.Vector((0, 0, 0)); d = (cam.matrix_world @ p) - o
    m = bpy.data.objects[namn]; inv = m.matrix_world.inverted()
    o2 = inv @ o; d2 = (inv @ (o + d)) - o2
    t = -o2.z / d2.z; q = o2 + d2 * t; return (round(q.x, 4), round(q.y, 4))

def star(farg, p, W, H, ljus=None, amb=0.25, golvfarg=None, vagg=None):
    # telefonen står på underkanten; golv = skuggfångare (eller riktigt golv om golvfarg/material ges)
    ny_scen(W, H); r = telefon(farg, p); material_fix(); kamera(p, W, H)
    if golvfarg is None:
        g = plan('golv', 4, (0, -0.0828, 0), (-90, 0, 0), r, mat_enkel((0.5, 0.5, 0.5))); g.is_shadow_catcher = True
    else:
        gm = golvfarg() if callable(golvfarg) else mat_enkel(golvfarg, 0.35)
        plan('golv', 4, (0, -0.0828, 0), (-90, 0, 0), r, gm)
    if vagg is not None:
        vm = vagg[1]() if callable(vagg[1]) else mat_enkel(vagg[1], 0.6)
        plan('vagg', 4, (0, 1.9, vagg[0]), (0, 0, 0), r, vm)
    for nm, lok, e, s, *f in (ljus or [('nyckel', (-0.35, 0.25, 0.45), 20, 0.6), ('kant', (0.4, 0.2, -0.3), 14, 0.4), ('fyll', (0.2, 0.0, 0.6), 4, 1.2)]):
        lokalt_ljus(r, nm, lok, e, s, *(f or [(1, 1, 1)]), mal=(0, 0, 0.005))
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.6, 0.62, 0.66, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = amb
    return r
