# Ref 54 ("Rain. Handled."): telefonen ligger i vått gräs på en sluttning, vattendroppar på skalet, skärpedjup.
import bpy, math, mathutils, random
L = {}; exec(open('/Users/george/Library/CloudStorage/GoogleDrive-contact@reborndevice.com/Min enhet/n8n Projekt Chat/Chat Robotfiler/_system/rdlib.py').read(), L)
p = [-22.206, 11.7386, -13.2716, 116.355, -0.0073988, 0.0442737]
FARG = globals().get('FARG', 'black')
def jord():
    m, nt, b = L['nmat']('jord'); v = L['koord'](nt)
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 40; n.inputs['Detail'].default_value = 8; nt.links.new(v, n.inputs['Vector'])
    c = L['ramp'](nt, n.outputs['Fac'], [(0.3, (0.012, 0.014, 0.006)), (0.6, (0.04, 0.045, 0.015)), (0.8, (0.08, 0.075, 0.03))]); nt.links.new(c, b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.35; L['bump'](nt, b, n.outputs['Fac'], 0.6, 0.003); return m
r = L['ligger'](FARG, p, 1080, 1920, jord, ljus=[('nyckel', (-0.2, 0.6, 0.5), 25, 1.5, (0.9, 0.95, 1.0)), ('fyll', (0.4, -0.3, 0.5), 6, 2)], amb=0.9)
mark = bpy.data.objects['mark']; mark.location.z = -0.03
# gräs
gm, gnt, gb = L['nmat']('gras')
hi = gnt.nodes.new('ShaderNodeHairInfo')
gc = L['ramp'](gnt, hi.outputs['Random'], [(0.0, (0.05, 0.07, 0.01)), (0.4, (0.13, 0.15, 0.03)), (0.7, (0.25, 0.22, 0.07)), (1.0, (0.35, 0.3, 0.12))])
gnt.links.new(gc, gb.inputs['Base Color']); gb.inputs['Roughness'].default_value = 0.3; gb.inputs['Specular IOR Level'].default_value = 0.8
bpy.ops.mesh.primitive_plane_add(size=1.2); gp = bpy.context.object; gp.parent = mark; gp.location = (0, 0, -0.0002)
gp.data.materials.append(gm); gp.data.materials.append(gm)
gp.modifiers.new('ps', 'PARTICLE_SYSTEM'); ps = gp.particle_systems[0].settings
ps.type = 'HAIR'; ps.count = 60000; ps.hair_length = 0.036; ps.use_advanced_hair = True
ps.child_type = 'INTERPOLATED'; ps.child_percent = 6; ps.rendered_child_count = 6; ps.child_length = 0.9; ps.child_length_threshold = 0.4
ps.roughness_1 = 0.02; ps.roughness_2 = 0.03; ps.roughness_endpoint = 0.02
ps.normal_factor = 0.04; ps.factor_random = 0.04; ps.brownian_factor = 0.0
ps.root_radius = 0.0007; ps.tip_radius = 0.0; ps.radius_scale = 1.0; ps.material_slot = 'gras'
ps.display_step = 3; ps.render_step = 4
# ingen gräs under telefonen (vikt via vertexgrupp är krångligt; vi lägger telefonen ovanpå, gräset böjs inte men syns runt)
# droppar på skalets baksida
dm, dnt, db = L['nmat']('droppe'); db.inputs['Transmission Weight'].default_value = 1.0; db.inputs['Roughness'].default_value = 0.02; db.inputs['IOR'].default_value = 1.33
random.seed(7)
for i in range(38):
    x = random.uniform(-0.035, 0.035); y = random.uniform(-0.075, 0.04)
    rr = random.uniform(0.0008, 0.0022)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=24, ring_count=12); d = bpy.context.object; bpy.ops.object.shade_smooth()
    d.parent = r; d.location = (x, y, 0.0113); d.scale = (rr, rr * random.uniform(0.9, 1.2), rr * 0.55); d.data.materials.append(dm)
# skärpedjup
cam = bpy.context.scene.camera; cam.data.dof.use_dof = True; cam.data.dof.focus_distance = 1.0; cam.data.dof.aperture_fstop = 3.5
