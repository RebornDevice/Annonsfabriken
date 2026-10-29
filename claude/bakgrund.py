# Procedurella bakgrunder (gradient + mjukt sken + korn) och ihopläggning med Blender-renderingar
import numpy as np
from PIL import Image, ImageFilter
def grad(W,H,topp,botten,sken=None,seed=1,korn=1.4,vinj=0.25):
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); t=(yy/H)[...,None]
    a=np.array(topp,np.float32)*(1-t)+np.array(botten,np.float32)*t
    for (cx,cy,rx,ry,farg,st) in (sken or []):
        r=np.sqrt(((xx-cx*W)/(rx*W))**2+((yy-cy*H)/(ry*H))**2); g=np.clip(1-r,0,1)**2
        a+=g[...,None]*np.array(farg,np.float32)*st
    r=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); a*=(1-vinj*np.clip(r-0.5,0,1))[...,None]
    a+=np.random.default_rng(seed).normal(0,korn,a.shape)
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert('RGBA')
def skugga(bg,tel,dx=0,dy=30,blur=35,styrka=0.35):
    sh=tel.split()[-1].filter(ImageFilter.GaussianBlur(blur)).point(lambda v:int(v*styrka))
    bg.paste((0,0,0,255),(dx,dy),sh); return bg
def tyg(W,H,farg,seed=4):
    # mjuka diagonala veck (läder-/tygkänsla)
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); u=(xx*0.6+yy*0.8)/W
    v=0.5+0.5*np.sin(u*7+np.sin(u*3.1)*1.5)*np.cos((xx-yy)/W*2.3)
    img=Image.fromarray((v*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(25)); v=np.asarray(img).astype(np.float32)/255
    a=np.array(farg,np.float32)[None,None,:]*(0.35+0.9*v[...,None])
    a+=np.random.default_rng(seed).normal(0,1.5,a.shape)
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert('RGBA')
