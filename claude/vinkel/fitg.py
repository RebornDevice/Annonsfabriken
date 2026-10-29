import bpy, math, mathutils, json, sys, numpy as np
from scipy.optimize import minimize
from PIL import Image
# fitg.py <refmask> <glb> <startjson> <maxfev> <ut_overlay>
refp,glb,p0,mf,ovp=sys.argv[1:6]
R=Image.open(refp); RW,RH=R.size; sc=300/max(RW,RH); W,H=max(2,round(RW*sc)),max(2,round(RH*sc))
ref=np.asarray(R.resize((W,H),Image.NEAREST))>0
bpy.ops.wm.read_factory_settings(use_empty=True)
fore=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=glb)
root=bpy.data.objects.new('root',None); bpy.context.scene.collection.objects.link(root)
for o in set(bpy.data.objects)-fore:
    if o.parent is None and o!=root: o.parent=root
s=bpy.context.scene; s.render.engine='BLENDER_WORKBENCH'; s.render.film_transparent=True
s.render.resolution_x=W; s.render.resolution_y=H; s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGBA'
c=bpy.data.cameras.new('c'); c.sensor_fit='VERTICAL' if RH>=RW else 'HORIZONTAL'; c.sensor_height=36; c.sensor_width=36
cam=bpy.data.objects.new('cam',c); s.collection.objects.link(cam); s.camera=cam
cam.location=(0,-1.0,0); cam.rotation_euler=(math.radians(90),0,0)
ut=ovp+'.sil.png'
def satt(p):
    rx,ry,rz,lens,sx,sy=[float(v) for v in p]
    root.rotation_euler=(math.radians(90+rx),math.radians(ry),math.radians(rz)); c.lens=lens; c.shift_x=sx; c.shift_y=sy
def sil(p):
    satt(p); s.render.filepath=ut; bpy.ops.render.render(write_still=True); return np.asarray(Image.open(ut))[...,3]>128
def kost(p):
    a=sil(p); return 1-(a&ref).sum()/(a|ref).sum()
best=None
for p in json.loads(p0):
    p=np.array(p,float); st=np.array([8,8,10,20,0.04,0.04]); sim=np.vstack([p]+[p+np.eye(6)[i]*st[i] for i in range(6)])
    r=minimize(kost,p,method='Nelder-Mead',options={'maxfev':int(mf),'xatol':0.01,'fatol':1e-4,'initial_simplex':sim})
    print('TRY',json.dumps(r.x.tolist()),round(1-r.fun,3),flush=True)
    if best is None or r.fun<best.fun: best=r
a=sil(best.x); print('RESULT',json.dumps(best.x.tolist()),'IoU',round(1-best.fun,3))
Image.fromarray(np.dstack([ref*255,a*255,np.zeros_like(a)]).astype(np.uint8)).save(ovp)
