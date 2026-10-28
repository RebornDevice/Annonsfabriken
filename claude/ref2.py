# Annonser som härmar specifika referenser. Sparar PSD+JPG + jämförelse (referens | vår).
import os,sys,json,glob,subprocess,tempfile,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import design as d
from PIL import Image, ImageOps, ImageDraw
import numpy as np
SYS=d.SYS; ROOT=d.ROOT; MAT=ROOT+'/Chat Material'
d.FONT=lambda w,s: d.ImageFont.truetype(f'{SYS}/fonts/{w}.ttf',int(s))
class Same(dict):
    def __missing__(s,k): return k
d.PSNAME=Same()
UT=ROOT+'/Chat Färdiga bilder/2026-10-28/referensstil-blender'; os.makedirs(UT,exist_ok=True)
REFS=sorted(glob.glob(ROOT+'/Chat Referensbilder/*'))
def crop_orig(f,x0,x1,ar,ext_top=0.0):
    im=Image.open(f'{MAT}/{f}'); im=im.convert('RGB'); W,H=im.size
    if ext_top:
        band=int(H*ext_top); pw=int(W*0.27); patch=im.crop((0,0,pw,band)).transpose(Image.FLIP_TOP_BOTTOM)
        top=Image.new('RGB',(W,band)); x=0; i=0
        while x<W: top.paste(patch if i%2==0 else patch.transpose(Image.FLIP_LEFT_RIGHT),(x,0)); x+=pw; i+=1
        ref=np.asarray(im.crop((0,0,W,int(band*.15)))).mean((0,1)); cur=np.asarray(top.crop((0,band-int(band*.15),W,band))).mean((0,1))
        top=Image.fromarray(np.clip(np.asarray(top).astype(np.float32)*(ref/cur),0,255).astype(np.uint8))
        n=Image.new('RGB',(W,H+band)); n.paste(top,(0,0)); n.paste(im,(0,band))
        f=int(band*.25); m=Image.fromarray((np.linspace(0,255,f)[:,None].repeat(W,1)).astype(np.uint8))
        n.paste(im.crop((0,0,W,f)).transpose(Image.FLIP_TOP_BOTTOM),(0,band-f),m)
        im=n; H+=band
    x0,x1=int(W*x0),int(W*x1); w=x1-x0; h=int(w/ar)
    if h>H: h=H; w=int(h*ar)
    y0=H-h; return im.crop((x0,y0,x0+w,y0+h))
def src(k):
    fs=sorted(glob.glob(ROOT+f'/Chat AI-råbilder/ai-X-{k}-*.png')); return Image.open(fs[-1])
BL=SYS+'/blender/'
def bg_fit(im,W,H):
    im=im.convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(im.width-W)//2; y=(im.height-H)//2; return im.crop((x,y,x+W,y+H))
def spara(D,namn):
    platt=D.bg.convert('RGBA')
    for l in D.lager: platt.alpha_composite(l['img'])
    platt.convert('RGB').save(f'{UT}/{namn}.jpg',quality=93)
    tmp=tempfile.mkdtemp(); D.bg.save(f'{tmp}/bg.png'); platt.save(f'{tmp}/platt.png')
    spec={'bredd':D.W,'hojd':D.H,'platt':'platt.png','ut':f'{UT}/{namn}.psd','lager':[{'namn':'Bild','fil':'bg.png'}]}
    for i,l in enumerate(D.lager):
        f=f'l{i}.png'; l['img'].save(f'{tmp}/{f}'); e={'namn':l['namn'],'fil':f}
        if l.get('text'): e['text']=l['text']
        spec['lager'].append(e)
    json.dump(spec,open(f'{tmp}/spec.json','w'))
    r=subprocess.run(['node',f'{SYS}/mkpsd.js',tmp],env={**os.environ,'NODE_PATH':os.path.expanduser('~/psdnode/node_modules')},capture_output=True,text=True)
    if r.returncode: print(r.stderr[-500:])
    shutil.rmtree(tmp); return platt.convert('RGB')
def jamfor(refnr,var,namn):
    ref=Image.open(REFS[refnr-1]).convert('RGB'); H=1100
    a=ref.resize((int(ref.width*H/ref.height),H)); b=var.resize((int(var.width*H/var.height),H))
    c=Image.new('RGB',(a.width+b.width+60,H+70),'white'); c.paste(a,(20,50)); c.paste(b,(a.width+40,50))
    dr=ImageDraw.Draw(c); f=d.FONT('Inter-Medium',28)
    dr.text((20,12),f'Referens {refnr}',font=f,fill='black'); dr.text((a.width+40,12),'Reborn (vår)',font=f,fill='black')
    c.save(f'{UT}/jamfor-{namn}.jpg',quality=88)
u=1080/1000
def bredd(s,f,st): return ImageDraw.Draw(Image.new('L',(1,1))).textlength(s,font=d.FONT(f,st))
def logo(D,bredd,x,y,just='center',ton=None):
    D.logo(bredd,x,y,just)
WHITE=(255,255,255)
# 1 Nudient "Slice Case" (ref 6) <- Blender-render (orange) + AI-betong
def r1():
    bg=d.grade(bg_fit(src('r06'),1080,1920))
    D=d.Design(bg,'D'); D.scrim(True,.32,150); W,H=D.W,D.H
    logo(D,230,W/2,H*.135)
    D.text('Produktnamn',['RD Case V4'],'Jost-Regular',66,W/2,H*.215)
    D.text('Underrad',['Available exclusively for iPhone 18 Pro Max'],'Jost-Regular',31,W/2,H*.26,alpha=235)
    return D,6,'1-nudient-slice'
# 2 Mous "Super thin" (ref 13) <- foto närbild + AI-förlängning
def r2():
    bg=d.grade(bg_fit(Image.open(BL+'f_mous_side.png'),1080,1920))
    D=d.Design(bg,'D'); D.scrim(True,.3,170); W,H=D.W,D.H
    logo(D,190,W/2,H*.078)
    D.text('Kicker',['NEW FOR IPHONE 18 PRO MAX'],'Oswald-Medium',38,W/2,H*.152,farg=(232,92,40),spärr=5)
    st=D.fit('SUPER THIN. 37 MAGNETS.','Oswald-SemiBold',86,W*.8)
    D.text('Rubrik',['SUPER THIN. 37 MAGNETS.'],'Oswald-SemiBold',st,W/2,H*.152+st*1.08)
    return D,13,'2-mous-super-thin'
# 3 Nudient "New Arrival" närbild (ref 20) <- riktigt foto, tät beskärning
def r3():
    im=Image.open(BL+'close2.png')
    bg=d.grade(bg_fit(im,1080,1920)); D=d.Design(bg,'D'); D.scrim(True,.16,120); W,H=D.W,D.H; m=W*.085
    D.text('Rubrik',['New Arrival'],'Jost-Regular',66,m,H*.06,just='left')
    D.text('Underrad',['RD Case V4','for iPhone 18 Pro Max'],'Jost-Regular',28,m,H*.06+46,just='left',radavst=1.25,alpha=235)
    logo(D,180,W-m-180,H*.06-36,just='left')
    D.text('Tillgänglig',['Available now'],'Jost-Regular',28,W-m-bredd('Available now','Jost-Regular',28),H*.06+46,just='left',alpha=235)
    return D,20,'3-nudient-new-arrival'
def ImageChops_offset(img,dx):
    c=Image.new('RGBA',img.size,(0,0,0,0)); c.alpha_composite(img,(max(dx,0),0) if dx>=0 else (0,0),(max(-dx,0),0)); return c
# 4 Nudient på grus (ref 29) <- riktigt foto på matta, förlängd uppåt
def r4():
    im=src('r29')
    bg=d.grade(bg_fit(im,1080,1920)); D=d.Design(bg,'D'); D.scrim(True,.38,140); W,H=D.W,D.H; m=W*.085
    D.text('Rubrik',['New Arrival'],'Jost-Regular',66,m,H*.13,just='left')
    D.text('Underrad',['RD Case V4','in White'],'Jost-Regular',30,m,H*.13+52,just='left',radavst=1.25,alpha=230)
    logo(D,190,W-m-190,H*.13-40,just='left')
    D.text('Säsong',['Autumn/Winter 2026'],'Jost-Regular',30,W-m-bredd('Autumn/Winter 2026','Jost-Regular',30),H*.13+52,just='left',alpha=230)
    return D,29,'4-nudient-grus'
# 5 Peel "Your iPhone. Just ..." (ref 56) <- riktigt foto (vitt skal) + AI-förlängning
def r5():
    bg=d.grade(bg_fit(src('r56'),1080,1920))
    D=d.Design(bg,'D'); D.scrim(True,.32,150); W,H=D.W,D.H; m=W*.1
    D.text('Rubrik',['Your iPhone.','Just Thinner.'],'Inter-Medium',92,m,H*.1,just='left',radavst=1.1)
    D.text('Fakta',['1 mm  Super thin'],'Inter-Regular',34,m,H*.1+92*1.1+95,just='left')
    logo(D,220,m,H*.92,just='left')
    return D,56,'5-peel-just-thinner'
# 6 Bullstrap "New & improved" (ref 18) <- AI ljus studio
def r6():
    bg=d.grade(bg_fit(src('r18'),1080,1920))
    D=d.Design(bg,'L'); W,H=D.W,D.H; m=W*.075; D.ink=(25,25,28)
    D.text('Rubrik',['NEW &','IMPROVED','FOR THE','IPHONE 18','PRO MAX'],'LexendZetta-Medium',44,m,H*.07,just='left',radavst=1.45)
    D.text('Botten',['THE RD CASE V4 BY RDEVICE'],'LexendZetta-Medium',24,W/2,H*.95,spärr=3)
    return D,18,'6-bullstrap-new-improved'
if __name__=='__main__':
    for fn in [r1,r2,r3,r4,r5,r6][int(sys.argv[1]) if len(sys.argv)>1 else 0:]:
        try:
            D,rn,namn=fn(); v=spara(D,namn); jamfor(rn,v,namn); print('KLAR',namn)
        except Exception as e: import traceback; traceback.print_exc()
