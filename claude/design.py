# Claude-delen: designar annonser (PSD med lager + JPG) av AI-råbilder och riktiga foton.
# Körs: python3 design.py [antal_riktiga_foton]
import os, sys, json, random, re, subprocess, shutil, datetime, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.expanduser('~/mnt/n8n Projekt Chat'); SYS=ROOT+'/Chat Robotfiler/_system'; RF=ROOT+'/Chat Robotfiler'
RAW=ROOT+'/Chat AI-råbilder'; UT=ROOT+'/Chat Färdiga bilder'
FONT=lambda w,s: ImageFont.truetype(f'{SYS}/fonts/Poppins-{w}.ttf',s)
PSNAME={'Bold':'Poppins-Bold','SemiBold':'Poppins-SemiBold','Medium':'Poppins-Medium','Regular':'Poppins-Regular','Light':'Poppins-Light'}
LOGO={'D':Image.open(ROOT+'/Chat Logga/Vit logga.png').convert('RGBA'),'L':Image.open(ROOT+'/Chat Logga/Svart logga.png').convert('RGBA')}
man={json.loads(l)['k']:json.loads(l) for l in open(f'{SYS}/manifest.jsonl')}
klar_f=f'{SYS}/klara.txt'; klara=set(open(klar_f).read().split()) if os.path.exists(klar_f) else set()
# --- texter (regler: engelska, bara 1 mm / 37 N52-magneter / MagSafe-Qi2, inget om material) ---
RUB=['Super thin.','Thin enough to forget.','1 mm. Nothing more.','37 magnets. Zero bulk.','Protection, refined.','Your iPhone. Just thinner.','Barely there.','Thin is the new strong.','Snaps on. Stays on.']
KICK=['NEW · RD CASE V4','1 MM THIN · 37 MAGNETS','MAGSAFE · QI2','37 N52 MAGNETS','THE RD CASE V4']
def modell(k):
    src=man.get(k,{}).get('src','')
    m=re.search(r'(iPhone [0-9A-Za-z ]+?)(?:/|$)',src)
    if src.startswith('3D Modeller/18 Pro Max'): return 'iPhone 18 Pro Max'
    return m.group(1).strip() if m else None
# --- bildbehandling ---
def grade(im):
    a=np.asarray(im.convert('RGB')).astype(np.float32)/255
    a=np.clip(0.5+(a-0.5)*1.08,0,1)                       # lite kontrast
    g=a.mean(2,keepdims=True); a=g+(a-g)*0.92               # lite mindre mättnad
    h,w=a.shape[:2]; yy,xx=np.mgrid[0:h,0:w]; r=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2)
    a*=(1-0.22*np.clip(r-0.55,0,1)**1.5)[...,None]           # vinjett
    a+=np.random.default_rng(1).normal(0,0.012,a.shape[:2])[...,None]  # filmkorn
    return Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
def lum(im,box): return float(np.asarray(im.convert('L').crop(box)).mean()/255)
class Design:
    def __init__(s,bg,ton): s.bg=bg; s.W,s.H=bg.size; s.ton=ton; s.lager=[]; s.u=s.W/1000; s.ink=(255,255,255) if ton=='D' else (14,14,16); s.soft=s.ink; s.acc=(120,170,255) if ton=='D' else (35,80,200)
    def canvas(s): return Image.new('RGBA',(s.W,s.H),(0,0,0,0))
    def text(s,namn,rader,vikt,storlek,x,y,just='center',farg=None,alpha=255,spärr=0,radavst=1.12):
        farg=farg or s.ink; f=FONT(vikt,int(storlek)); c=s.canvas(); d=ImageDraw.Draw(c); lead=storlek*radavst
        for i,r in enumerate(rader):
            yy=y+i*lead
            if spärr:
                tot=sum(d.textlength(ch,font=f) for ch in r)+spärr*(len(r)-1); xx=x-tot/2 if just=='center' else x
                for ch in r: d.text((xx,yy),ch,font=f,fill=farg+(alpha,),anchor='ls'); xx+=d.textlength(ch,font=f)+spärr
            else: d.text((x,yy),r,font=f,fill=farg+(alpha,),anchor='ms' if just=='center' else 'ls')
        s.lager.append({'namn':namn,'img':c,'text':{'rader':rader,'font':PSNAME[vikt],'storlek':int(storlek),'farg':list(farg),'x':x,'y':y,'just':just,'radavstand':lead,'spärr':round(spärr/storlek*1000) if spärr else 0}})
    def fit(s,t,vikt,storlek,maxw):
        d=ImageDraw.Draw(s.canvas())
        while d.textlength(t,font=FONT(vikt,int(storlek)))>maxw and storlek>20: storlek-=2
        return storlek
    def wrap(s,t,vikt,storlek,maxw):
        d=ImageDraw.Draw(s.canvas()); f=FONT(vikt,int(storlek)); rader=[]; cur=''
        for w in t.split():
            if d.textlength((cur+' '+w).strip(),font=f)>maxw and cur: rader.append(cur); cur=w
            else: cur=(cur+' '+w).strip()
        return rader+[cur]
    def logo(s,bredd,x,y,just='center'):
        lg=LOGO[s.ton]; bw=int(bredd); lg=lg.resize((bw,int(lg.height*bw/lg.width)),Image.LANCZOS); c=s.canvas()
        c.alpha_composite(lg,(int(x-bw/2) if just=='center' else int(x),int(y))); s.lager.append({'namn':'Logga RDEVICE','img':c})
    def scrim(s,topp=True,h=.36,styrka=110):
        c=s.canvas(); col=(0,0,0) if s.ton=='D' else (255,255,255); hh=int(s.H*h)
        g=np.linspace(1,0,hh)**1.8*styrka; m=Image.fromarray(np.repeat(g[:,None],s.W,1).astype(np.uint8))
        if not topp: m=m.transpose(Image.FLIP_TOP_BOTTOM)
        lay=Image.new('RGBA',(s.W,hh),col+(0,)); lay.putalpha(m); c.alpha_composite(lay,(0,0 if topp else s.H-hh))
        s.lager.insert(0,{'namn':'Toning','img':c})
# --- mallar i referensstil ---
def mall_nudient(D,k):
    u=D.u; D.scrim(True,.3,90); D.logo(130*u,D.W/2,D.H*.05)
    D.text('Produktnamn',['RD Case V4'],'Regular',58*u,D.W/2,D.H*.05+130*u)
    mod=modell(k); D.text('Underrad',[f'Available for {mod}' if mod else 'MagSafe · Qi2 compatible'],'Regular',27*u,D.W/2,D.H*.05+180*u,alpha=215)
def mall_mous(D,k):
    u=D.u; D.scrim(True,.36,120); D.logo(120*u,D.W/2,D.H*.04)
    D.text('Kicker',[random.choice(KICK)],'SemiBold',24*u,D.W/2,D.H*.04+95*u,farg=D.acc,spärr=4*u)
    t=random.choice(RUB).upper(); st=D.fit(t,'Bold',92*u,D.W*.88)
    rader=[t] if st>70*u else D.wrap(t,'Bold',92*u,D.W*.86); st=st if len(rader)==1 else 92*u
    D.text('Rubrik',rader,'Bold',st,D.W/2,D.H*.04+95*u+st*1.05,radavst=1.0)
def mall_nu(D,k):
    u=D.u; D.scrim(True,.3,100); D.scrim(False,.14,90)
    st=D.fit('RD CASE V4','Bold',84*u,D.W*.86); D.text('Titel',['RD CASE V4'],'Bold',st,D.W/2,D.H*.05+st)
    mod=modell(k); D.text('Modell',[f'for {mod}' if mod else 'MagSafe · Qi2'],'Regular',32*u,D.W/2,D.H*.05+st+48*u)
    D.logo(150*u,D.W/2,D.H*.94-25*u)
def mall_peel(D,k):
    u=D.u; m=D.W*.075; D.scrim(True,.4,120); D.scrim(False,.14,90)
    t=random.choice([r for r in RUB if len(r)>12]); rader=D.wrap(t,'Medium',80*u,D.W*.62)
    D.text('Rubrik',rader,'Medium',80*u,m,D.H*.06+80*u,just='left',radavst=1.1)
    D.text('Fakta',['1 mm thin · 37 N52 magnets'],'Regular',28*u,m,D.H*.06+80*u+len(rader)*88*u+20*u,just='left',alpha=215)
    D.logo(140*u,m,D.H*.94-25*u,just='left')
def mall_casetify(D,k):
    u=D.u; m=D.W*.07; D.scrim(True,.33,120); D.scrim(False,.24,120)
    t=random.choice(['BUILT THIN.','SUPER THIN.','BARELY THERE.','SNAPS ON.']); 
    D.text('Rubrik',[t],'Bold',D.fit(t,'Bold',110*u,D.W*.86),m,D.H*.05+105*u,just='left')
    D.text('Fakta',['1 MM THIN','37 N52 MAGNETS','MAGSAFE · QI2'],'SemiBold',24*u,m,D.H*.84,just='left',radavst=1.3)
    mod=modell(k); D.text('Ny',[f'NEW FOR {mod.upper()}' if mod else 'NEW · RD CASE V4'],'Bold',30*u,m,D.H*.84+100*u,just='left')
    D.logo(150*u,D.W-m-150*u,D.H*.94-20*u,just='left')
MALLAR=[mall_nudient,mall_mous,mall_nu,mall_peel,mall_casetify]
def bygg(bg_path,k,namn,story):
    bg=Image.open(bg_path).convert('RGB'); W,H=(1080,1920) if story else (1080,1350)
    bg=bg.resize((W,int(bg.height*W/bg.width)),Image.LANCZOS)
    if bg.height!=H: y=(bg.height-H)//2; bg=bg.crop((0,max(0,y),W,max(0,y)+H)) if bg.height>H else bg.resize((W,H))
    bg=grade(bg); ton='L' if lum(bg,(0,0,W,int(H*.3)))>.56 else 'D'
    D=Design(bg,ton); random.choice(MALLAR)(D,k)
    platt=bg.convert('RGBA')
    for l in D.lager: platt.alpha_composite(l['img'])
    dag=datetime.date.today().isoformat(); ud=f'{UT}/{dag}'; os.makedirs(ud,exist_ok=True)
    platt.convert('RGB').save(f'{ud}/{namn}.jpg',quality=93)
    tmp=tempfile.mkdtemp(); bg.save(f'{tmp}/bg.png'); platt.save(f'{tmp}/platt.png')
    spec={'bredd':W,'hojd':H,'platt':'platt.png','ut':f'{ud}/{namn}.psd','lager':[{'namn':'Bild','fil':'bg.png'}]}
    for i,l in enumerate(D.lager):
        f=f'l{i}.png'; l['img'].save(f'{tmp}/{f}'); e={'namn':l['namn'],'fil':f}
        if l.get('text'): e['text']=l['text']
        spec['lager'].append(e)
    json.dump(spec,open(f'{tmp}/spec.json','w'))
    subprocess.run(['node',f'{SYS}/mkpsd.js',tmp],check=True,env={**os.environ,'NODE_PATH':os.path.expanduser('~/psdnode/node_modules')},capture_output=True)
    shutil.rmtree(tmp); return f'{ud}/{namn}.jpg'
if __name__=='__main__':
    n_foto=int(sys.argv[1]) if len(sys.argv)>1 else 3
    gjorda=[]
    for f in sorted(os.listdir(RAW)):
        m=re.match(r'ai-(A|C)-(s\d+)-',f)
        if not m or f in klara: continue
        try: gjorda.append(bygg(f'{RAW}/{f}',m.group(2),'rd-'+f[3:-4],m.group(1)=='C')); klara.add(f)
        except Exception as e: print('FEL',f,e)
    foton=[f for f in os.listdir(RF) if f.startswith('B_bild_s') and f not in klara]
    for f in random.sample(foton,min(n_foto,len(foton))):
        k=f.split('_')[2]
        try: gjorda.append(bygg(f'{RF}/{f}',k,f'rd-foto-{k}-{datetime.datetime.now():%H%M}',False)); klara.add(f)
        except Exception as e: print('FEL',f,e)
    open(klar_f,'w').write('\n'.join(sorted(klara)))
    for g in gjorda: print('KLAR',g)
