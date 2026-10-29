import bpy, math, mathutils, json, sys, numpy as np
from scipy.optimize import minimize
from PIL import Image
W,H=169,300
ref=np.asarray(Image.open('/tmp/claude-0/r/pnp/refsil.png').resize((W,H),Image.NEAREST))>0
rside=np.asarray(Image.open('/tmp/claude-0/r/pnp/refside.png').resize((W,H),Image.NEAREST))>0
bpy.ops.wm.read_factory_settings(use_empty=True)
fore=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath='/tmp/claude-0/r/black.glb')
root=bpy.data.objects.new('root',None); bpy.context.scene.collection.objects.link(root)
for o in set(bpy.data.objects)-fore:
    if o.parent is None and o!=root: o.parent=root
s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.samples=1; s.cycles.use_denoising=False; s.render.film_transparent=True
s.view_settings.view_transform='Standard'
s.render.resolution_x=W; s.render.resolution_y=H; s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGBA'
s.cycles.max_bounces=0
m=bpy.data.materials.new('ov'); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
geo=nt.nodes.new('ShaderNodeNewGeometry'); dot=nt.nodes.new('ShaderNodeVectorMath'); dot.operation='DOT_PRODUCT'
gt=nt.nodes.new('ShaderNodeMath'); gt.operation='GREATER_THAN'; gt.inputs[1].default_value=0.6
em=nt.nodes.new('ShaderNodeEmission'); out=nt.nodes.new('ShaderNodeOutputMaterial')
nt.links.new(geo.outputs['Normal'],dot.inputs[0]); nt.links.new(dot.outputs['Value'],gt.inputs[0]); nt.links.new(gt.outputs[0],em.inputs['Color']); nt.links.new(em.outputs[0],out.inputs['Surface'])
bpy.context.view_layer.material_override=m
c=bpy.data.cameras.new('c'); c.sensor_fit='VERTICAL'; c.sensor_height=36
cam=bpy.data.objects.new('cam',c); s.collection.objects.link(cam); s.camera=cam
ut='/tmp/claude-0/r/pnp/sil4.png'
def satt(p):
    az,el,roll,lens,d,sx,sy,luta,tipp=[float(v) for v in p]
    root.rotation_euler=(math.radians(90+tipp),math.radians(luta),0); root.location=(0,0,0.0827)
    bpy.context.view_layer.update()
    ax=(root.matrix_world.to_3x3()@mathutils.Vector((1,0,0))).normalized()
    dot.inputs[1].default_value=ax
    ctr=mathutils.Vector((0,0,0.0827))
    pos=ctr+d*mathutils.Vector((math.sin(math.radians(az))*math.cos(math.radians(el)),-math.cos(math.radians(az))*math.cos(math.radians(el)),math.sin(math.radians(el))))
    cam.location=pos; dv=ctr-pos; cam.rotation_euler=dv.to_track_quat('-Z','Y').to_euler(); cam.rotation_euler.rotate_axis('Z',math.radians(roll))
    c.lens=lens; c.shift_x=sx; c.shift_y=sy
def rend(p):
    satt(p); s.render.filepath=ut; bpy.ops.render.render(write_still=True)
    a=np.asarray(Image.open(ut)); return a[...,3]>128, (a[...,0]>128)&(a[...,3]>128)
n=[0]; WS=float(sys.argv[3]); AZF=float(sys.argv[4]); ELF=float(sys.argv[5]) if len(sys.argv)>5 else None
def kost(p):
    a,sd=rend(p); n[0]+=1
    i1=(a&ref).sum()/(a|ref).sum(); i2=(sd&rside).sum()/max(1,(sd|rside).sum())
    return (1-i1)+WS*(1-i2)+(0.02*(float(p[0])-AZF)**2 if AZF else 0)+(0.05*(float(p[1])-ELF)**2 if ELF is not None else 0)
p0=np.array(json.loads(sys.argv[1]))
st=np.array([4,3,3,15,0.1,0.02,0.02,3,4]); sim=np.vstack([p0]+[p0+np.eye(len(p0))[i]*st[i] for i in range(len(p0))])
r=minimize(kost,p0,method='Nelder-Mead',options={'maxfev':int(sys.argv[2]),'xatol':0.01,'fatol':1e-4,'initial_simplex':sim})
a,sd=rend(r.x); i1=(a&ref).sum()/(a|ref).sum(); i2=(sd&rside).sum()/max(1,(sd|rside).sum())
print('RESULT',json.dumps(r.x.tolist()),'IoU',round(i1,3),'sida',round(i2,3),'evals',n[0])
Image.fromarray(np.dstack([ref*255,a*160+sd*95,rside*255]).astype(np.uint8)).save('/tmp/claude-0/r/pnp/overlay4.png')
