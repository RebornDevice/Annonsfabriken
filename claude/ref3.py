# Fler referensannonser (nr 16-). Använder hjälpfunktionerna i ref2.py.
# Kör: python3 ref3.py r16 [r17 ...]
import os, sys
_s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref2.py')).read().split("if __name" + "__")[0]
exec(compile(_s, 'ref2.py', 'exec'))

def new_arrival(D, farg, y=.178):
    W, H = D.W, D.H; m = W * .087; y = H * y
    D.text('Rubrik', ['New Arrival'], 'Jost-Regular', 56, m, y, just='left')
    D.text('Underrad', ['RD Case V4 in', farg], 'Jost-Regular', 26, m, y + 48, just='left', radavst=1.3)
    D.logo(175, W - m - 175, y - 26, just='left')
    hoger(D, 'Autumn/Winter 2026', 'Jost-Regular', 26, W - m, y + 48, namn='Säsong')

# 16 Nudient "New Arrival" på svart sand (ref 10)
def r16():
    bg = d.grade(bg_fit(src('r10mac').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D')
    new_arrival(D, 'Glacier White'); return D, 10, '16-new-arrival-sand'

# 17 Nudient "New Arrival" på sprucken lera med mossa (ref 15)
def r17():
    bg = d.grade(bg_fit(src('r15mac').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D')
    new_arrival(D, 'Deep Blue', y=.172); return D, 15, '17-new-arrival-lera'

# 18 Nudient "Slice Case" tre telefoner på grå gradient (ref 5)
def r18():
    bg = d.grade(bg_fit(src('r5mac').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.logo(165, W / 2, H * .147)
    D.text('Produktnamn', ['RD Case V4'], 'Jost-Regular', 62, W / 2, H * .214)
    D.text('Underrad', ['Available exclusively for iPhone 18 Pro Max'], 'Jost-Regular', 34, W / 2, H * .266, alpha=240)
    return D, 5, '18-tre-skal-gradient'

# 19 Nudient "Slice Case" på svart podium mot trävägg (ref 8)
def r19():
    bg = d.grade(bg_fit(src('r8mac').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H; m = W * .09
    D.logo(245, m, H * .148, just='left')
    D.text('Produktnamn', ['RD Case V4'], 'Jost-Regular', 54, m, H * .238, just='left')
    hoger(D, 'Just 1 mm thin.', 'Jost-Regular', 34, W - m, H * .238, namn='Fakta')
    return D, 8, '19-podium-travagg'

# 20 Skrivbordsbild ovanifrån med tangentbord, hörlurar och penna (ref 11) - bara bild, liten logga
def r20():
    bg = d.grade(bg_fit(src('r11mac').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.logo(150, W * .5, H * .955)
    return D, 11, '20-skrivbord-ovanifran'

# ---- Varianter (andra färger/texter) ----
def r21():  # ref 10, svart skal
    bg = d.grade(bg_fit(src('r10macB').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H; m = W * .087; y = H * .178
    D.text('Rubrik', ['Just 1 mm.'], 'Jost-Regular', 56, m, y, just='left')
    D.text('Underrad', ['RD Case V4 in', 'Black'], 'Jost-Regular', 26, m, y + 48, just='left', radavst=1.3)
    D.logo(175, W - m - 175, y - 26, just='left')
    hoger(D, 'MagSafe & Qi2', 'Jost-Regular', 26, W - m, y + 48, namn='Fakta')
    return D, 10, '21-variant-sand-svart'

def r22():  # ref 15, vitt skal
    bg = d.grade(bg_fit(src('r15macW').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H; m = W * .087; y = H * .172
    D.text('Rubrik', ['Barely there.'], 'Jost-Regular', 56, m, y, just='left')
    D.text('Underrad', ['RD Case V4 in', 'Glacier White'], 'Jost-Regular', 26, m, y + 48, just='left', radavst=1.3)
    D.logo(175, W - m - 175, y - 26, just='left')
    hoger(D, '37 N52 magnets', 'Jost-Regular', 26, W - m, y + 48, namn='Fakta')
    return D, 15, '22-variant-lera-vit'

def r23():  # ref 8, blått skal
    bg = d.grade(bg_fit(src('r8macB').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H; m = W * .09
    D.logo(245, m, H * .148, just='left')
    D.text('Produktnamn', ['RD Case V4'], 'Jost-Regular', 54, m, H * .238, just='left')
    hoger(D, '37 N52 magnets.', 'Jost-Regular', 34, W - m, H * .238, namn='Fakta')
    return D, 8, '23-variant-podium-bla'

def r24():  # ref 11, vitt skal på skrivbordet
    bg = d.grade(bg_fit(src('r11macW').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.logo(150, W * .5, H * .955)
    return D, 11, '24-variant-skrivbord-vit'

# 25 Native Union "Active Case" fyra skal på bord (ref 28)
def r25():
    bg = d.grade(bg_fit(src('r28mac').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['RD CASE V4'], 'Oswald-SemiBold', 108, W / 2, H * .175, spärr=2)
    D.text('Under', ['FOR IPHONE 18 PRO MAX'], 'Oswald-SemiBold', 34, W / 2, H * .228)
    D.logo(200, W / 2, H * .905)
    return D, 28, '25-fyra-skal-bord'

# 26 "Rain. Handled." i vått gräs (ref 54)
def r26():
    bg = d.grade(bg_fit(src('r54mac').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['BARELY.', 'THERE.'], 'Jost-Medium', 56, W * .5, H * .158, spärr=8, radavst=1.18)
    D.text('Under', ['RD Case V4 for iPhone 18 Pro Max'], 'Jost-Regular', 27, W * .5, H * .226, alpha=235)
    D.logo(150, W / 2, H * .94)
    return D, 54, '26-vatt-gras'

# 27 Mous "Perfect Match" svävande över klippa (ref 35)
def r27():
    bg = d.grade(bg_fit(src('r35mac').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.logo(190, W * .5, H * .352)
    D.text('Rubrik', ['ZERO BULK.'], 'Jost-SemiBold', 84, W * .5, H * .418, spärr=2)
    D.text('Under', ['1 MM THIN IN DEEP BLUE'], 'Jost-Medium', 27, W * .5, H * .456, spärr=4, alpha=235)
    return D, 35, '27-svavar-klippa'

# 28 Native Union "ReClassic" på plommonfärgat podium (ref 34)
def r28():
    bg = d.grade(bg_fit(src('r34mac').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['New iPhone 18 Pro Max'], 'Inter-Regular', 62, W / 2, H * .095)
    D.text('Under', ['RD Case V4 + MagSafe'], 'Inter-SemiBold', 40, W / 2, H * .158, farg=(214, 140, 190))
    D.logo(170, W / 2, H * .935)
    return D, 34, '28-plommon-podium'

# 29 Reklamskylt i stan (ref 40), 4:5
def r29():
    bg = d.grade(bg_fit(src('r40mac').convert('RGB'), 960, 1200)); D = d.Design(bg, 'L'); W, H = D.W, D.H; D.ink = (25, 28, 34)
    D.text('Skylt', ['Just 1 mm thin.'], 'Inter-Medium', 40, W * .5, H * .13)
    D.ink = (255, 255, 255)
    D.text('Rubrik', ['RD CASE V4'], 'Oswald-SemiBold', 64, W * .5, H * .925, spärr=2)
    D.text('Under', ['For iPhone 18 Pro Max'], 'Inter-Medium', 26, W * .5, H * .965, spärr=2)
    return D, 40, '29-reklamskylt-stad'

def r30():  # ref 40, svart skal
    bg = d.grade(bg_fit(src('r40macB').convert('RGB'), 960, 1200)); D = d.Design(bg, 'L'); W, H = D.W, D.H; D.ink = (25, 28, 34)
    D.text('Skylt', ['Barely there.'], 'Inter-Medium', 40, W * .5, H * .13)
    D.ink = (255, 255, 255)
    D.text('Rubrik', ['RD CASE V4'], 'Oswald-SemiBold', 64, W * .5, H * .925, spärr=2)
    D.text('Under', ['1 mm thin · MagSafe'], 'Inter-Medium', 26, W * .5, H * .965, spärr=2)
    return D, 40, '30-variant-skylt-svart'

def r31():  # ref 35, svart skal
    bg = d.grade(bg_fit(src('r35macB').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.logo(190, W * .5, H * .352)
    D.text('Rubrik', ['NOTHING EXTRA.'], 'Jost-SemiBold', 78, W * .5, H * .418, spärr=2)
    D.text('Under', ['1 MM THIN · 37 N52 MAGNETS'], 'Jost-Medium', 27, W * .5, H * .456, spärr=4, alpha=235)
    return D, 35, '31-variant-klippa-svart'

def r32():  # ref 54, vitt skal
    bg = d.grade(bg_fit(src('r54macW').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['SIMPLY.', 'THIN.'], 'Jost-Medium', 56, W * .5, H * .158, spärr=8, radavst=1.18)
    D.text('Under', ['37 N52 magnets · MagSafe & Qi2'], 'Jost-Regular', 27, W * .5, H * .226, alpha=235)
    D.logo(150, W / 2, H * .94)
    return D, 54, '32-variant-gras-vit'

def r33():  # ref 28, andra färger + annan text
    bg = d.grade(bg_fit(src('r28macB').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['1 MM THIN'], 'Oswald-SemiBold', 108, W / 2, H * .175, spärr=2)
    D.text('Under', ['RD CASE V4 · 37 N52 MAGNETS'], 'Oswald-SemiBold', 34, W / 2, H * .228)
    D.logo(200, W / 2, H * .905)
    return D, 28, '33-variant-fyra-skal'

def r34():  # ref 34, vitt skal
    bg = d.grade(bg_fit(src('r34macW').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['Made for iPhone 18 Pro Max'], 'Inter-Regular', 56, W / 2, H * .095)
    D.text('Under', ['RD Case V4 in Glacier White'], 'Inter-SemiBold', 38, W / 2, H * .158, farg=(214, 140, 190))
    D.logo(170, W / 2, H * .935)
    return D, 34, '34-variant-plommon-vit'

def r35():  # ref 15, svart skal
    bg = d.grade(bg_fit(src('r15macB').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D')
    W, H = D.W, D.H; m = W * .087; y = H * .172
    D.text('Rubrik', ['Built thin.'], 'Jost-Regular', 56, m, y, just='left')
    D.text('Underrad', ['RD Case V4 in', 'Black'], 'Jost-Regular', 26, m, y + 48, just='left', radavst=1.3)
    D.logo(175, W - m - 175, y - 26, just='left')
    hoger(D, '1 mm · MagSafe', 'Jost-Regular', 26, W - m, y + 48, namn='Fakta')
    return D, 15, '35-variant-lera-svart'

# 36 "Most cases fade." stående + liggande skal på salviagrönt (ref 50)
def r36():
    bg = d.grade(bg_fit(src('r50mac').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'L'); W, H = D.W, D.H; m = W * .045
    D.ink = (30, 32, 30)
    D.text('Rubrik 1', ['Most cases add bulk.'], 'PlayfairDisplay-Regular', 54, m, H * .093, just='left')
    D.text('Rubrik 2', ["Ours doesn't."], 'PlayfairDisplay-Italic', 54, m, H * .15, just='left', farg=(96, 70, 48))
    D.text('Modell', ['IPHONE 18 PRO MAX'], 'Inter-Regular', 30, m, H * .218, just='left', spärr=3)
    D.text('Leverans', ['SHIPPING NOW'], 'Inter-Medium', 20, m, H * .26, just='left', spärr=5, farg=(110, 80, 55))
    D.logo(150, W - m - 150, H * .955, just='left')
    return D, 50, '36-staende-liggande-salvia'

def r37():  # ref 10, blått skal
    bg = d.grade(bg_fit(src('r10macU').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H; m = W * .087; y = H * .178
    D.text('Rubrik', ['Deep Blue.'], 'Jost-Regular', 56, m, y, just='left')
    D.text('Underrad', ['RD Case V4', 'for iPhone 18 Pro Max'], 'Jost-Regular', 26, m, y + 48, just='left', radavst=1.3)
    D.logo(175, W - m - 175, y - 26, just='left')
    hoger(D, '37 N52 magnets', 'Jost-Regular', 26, W - m, y + 48, namn='Fakta')
    return D, 10, '37-variant-sand-bla'

def r38():  # ref 11, svart skal
    bg = d.grade(bg_fit(src('r11macB').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.logo(150, W * .5, H * .955)
    return D, 11, '38-variant-skrivbord-svart'

def r39():  # ref 8, vitt skal
    bg = d.grade(bg_fit(src('r8macW').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H; m = W * .09
    D.logo(245, m, H * .148, just='left')
    D.text('Produktnamn', ['Glacier White'], 'Jost-Regular', 54, m, H * .238, just='left')
    hoger(D, 'MagSafe & Qi2.', 'Jost-Regular', 34, W - m, H * .238, namn='Fakta')
    return D, 8, '39-variant-podium-vit'

def r40():  # ref 5, annan färgordning + text
    bg = d.grade(bg_fit(src('r5macB').convert('RGB'), 1080, 1920)); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.logo(165, W / 2, H * .147)
    D.text('Produktnamn', ['Three colors. One feel.'], 'Jost-Regular', 58, W / 2, H * .214)
    D.text('Underrad', ['1 mm thin · 37 N52 magnets · MagSafe'], 'Jost-Regular', 32, W / 2, H * .266, alpha=240)
    return D, 5, '40-variant-tre-skal'

def r41():  # ref 53, ljus studio, blått skal + sten
    bg = bg_fit(src('r53mac').convert('RGB'), 1080, 1920); D = d.Design(bg, 'L'); W, H = D.W, D.H
    D.ink = (20, 20, 22)
    D.text('Rubrik', ['Thin enough to forget,', 'strong enough to snap on.'], 'Jost-Regular', 76, W / 2, H * .125, radavst=1.15)
    D.text('Fakta', ['1 mm thin   •   37 N52 magnets   •   MagSafe & Qi2'], 'Jost-Regular', 38, W / 2, H * .79)
    D.logo(230, W / 2, H * .885)
    return D, 53, '41-studio-ljus-bla'

def r42():  # ref 53, svart skal
    bg = bg_fit(src('r53macB').convert('RGB'), 1080, 1920); D = d.Design(bg, 'L'); W, H = D.W, D.H
    D.ink = (20, 20, 22)
    D.text('Rubrik', ['All black.', 'Just 1 mm thin.'], 'Jost-Regular', 76, W / 2, H * .125, radavst=1.15)
    D.text('Fakta', ['RD Case V4   •   37 N52 magnets   •   MagSafe & Qi2'], 'Jost-Regular', 38, W / 2, H * .79)
    D.logo(230, W / 2, H * .885)
    return D, 53, '42-variant-studio-svart'

def r43():  # ref 53, vitt skal
    bg = bg_fit(src('r53macW').convert('RGB'), 1080, 1920); D = d.Design(bg, 'L'); W, H = D.W, D.H
    D.ink = (20, 20, 22)
    D.text('Rubrik', ['Clean white.', 'Snaps on with MagSafe.'], 'Jost-Regular', 76, W / 2, H * .125, radavst=1.15)
    D.text('Fakta', ['1 mm thin   •   37 N52 magnets   •   Qi2 ready'], 'Jost-Regular', 38, W / 2, H * .79)
    D.logo(230, W / 2, H * .885)
    return D, 53, '43-variant-studio-vit'

def r44():  # ref 50, vitt + orange skal
    bg = d.grade(bg_fit(src('r50macWO').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'L'); W, H = D.W, D.H; m = W * .045
    D.ink = (30, 32, 30)
    D.text('Rubrik 1', ['Most cases are thick.'], 'PlayfairDisplay-Regular', 54, m, H * .093, just='left')
    D.text('Rubrik 2', ['Ours is 1 mm.'], 'PlayfairDisplay-Italic', 54, m, H * .15, just='left', farg=(96, 70, 48))
    D.text('Modell', ['IPHONE 18 PRO MAX'], 'Inter-Regular', 30, m, H * .218, just='left', spärr=3)
    D.text('Leverans', ['SHIPPING NOW'], 'Inter-Medium', 20, m, H * .26, just='left', spärr=5, farg=(110, 80, 55))
    D.logo(150, W - m - 150, H * .955, just='left')
    return D, 50, '44-variant-salvia-vit-orange'

def r45():  # ref 30, fyra skal i diagonal rad
    bg = bg_fit(src('r30mac').convert('RGB'), 1080, 1080); D = d.Design(bg, 'L'); W, H = D.W, D.H
    D.ink = (12, 12, 14)
    D.text('Rubrik', ['iPhone 18 Pro Max'], 'Inter-Regular', 74, W / 2, H * .09)
    D.text('Underrad', ['RD Case V4'], 'Inter-Regular', 40, W / 2, H * .158, alpha=235)
    D.logo(200, W / 2, H * .925)
    return D, 30, '45-fyra-skal-rad'

def r46():  # ref 30, mörk variant, svart skal främst
    bg = bg_fit(src('r30macD').convert('RGB'), 1080, 1080); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['iPhone 18 Pro Max'], 'Inter-Regular', 74, W / 2, H * .09)
    D.text('Underrad', ['1 mm thin. 37 N52 magnets.'], 'Inter-Regular', 38, W / 2, H * .158, alpha=225)
    D.logo(200, W / 2, H * .925)
    return D, 30, '46-variant-fyra-skal-mork'

def r47():  # ref 33, fyra skal i solfjäder
    bg = bg_fit(src('r33mac').convert('RGB'), 1080, 1080); D = d.Design(bg, 'L'); W, H = D.W, D.H
    D.ink = (10, 10, 12)
    D.text('Rubrik', ['RD Case V4'], 'Poppins-Bold', 96, W / 2, H * .11)
    D.text('Underrad', ['for iPhone 18 Pro Max'], 'Poppins-SemiBold', 36, W / 2, H * .205)
    D.logo(190, W / 2, H * .885)
    return D, 33, '47-fyra-skal-solfjader'

def r48():  # ref 33, variant: svart främst, sandbeige bakgrund
    bg = bg_fit(src('r33macB').convert('RGB'), 1080, 1080); D = d.Design(bg, 'L'); W, H = D.W, D.H
    D.ink = (24, 20, 16)
    D.text('Rubrik', ['Black. Blue. White.'], 'Poppins-Bold', 92, W / 2, H * .11)
    D.text('Underrad', ['1 mm thin  ·  MagSafe  ·  iPhone 18 Pro Max'], 'Poppins-Medium', 32, W / 2, H * .205)
    D.logo(190, W / 2, H * .885)
    return D, 33, '48-variant-solfjader-sand'

def r49():  # ref 50, blått + vitt skal, varm terrakotta
    bg = d.grade(bg_fit(src('r50macBW').convert('RGB'), 1080, 1080)); D = d.Design(bg, 'L'); W, H = D.W, D.H; m = W * .045
    D.ink = (40, 26, 20)
    D.text('Rubrik 1', ['Most cases hide your iPhone.'], 'PlayfairDisplay-Regular', 50, m, H * .093, just='left')
    D.text('Rubrik 2', ["Ours is 1 mm thin."], 'PlayfairDisplay-Italic', 50, m, H * .148, just='left', farg=(250, 236, 222))
    D.text('Modell', ['IPHONE 18 PRO MAX'], 'Inter-Regular', 30, m, H * .218, just='left', spärr=3)
    D.text('Leverans', ['SHIPPING NOW'], 'Inter-Medium', 20, m, H * .26, just='left', spärr=5, farg=(250, 236, 222))
    D.logo(150, W - m - 150, H * .955, just='left')
    return D, 50, '49-variant-terrakotta-bla-vit'

def r50():  # ref 42, fyra liggande skal i diagonal rad
    bg = bg_fit(src('r42mac').convert('RGB'), 1080, 1350); D = d.Design(bg, 'L'); W, H = D.W, D.H
    D.ink = (14, 14, 16)
    D.text('Rubrik', ['RD CASE V4'], 'Inter-SemiBold', 104, W / 2, H * .175)
    D.text('Underrad', ['for iPhone 18 Pro Max'], 'Inter-Regular', 44, W / 2, H * .25)
    D.text('Fakta', ['1 mm thin  ·  37 N52 magnets  ·  MagSafe & Qi2'], 'Inter-Regular', 34, W / 2, H * .74, alpha=230)
    D.logo(200, W / 2, H * .91)
    return D, 42, '50-fyra-skal-liggande-rad'

def r51():  # ref 42, variant mörk grafit
    bg = bg_fit(src('r42macD').convert('RGB'), 1080, 1350); D = d.Design(bg, 'D'); W, H = D.W, D.H
    D.text('Rubrik', ['THIN BY DESIGN'], 'Inter-SemiBold', 96, W / 2, H * .175)
    D.text('Underrad', ['RD Case V4 for iPhone 18 Pro Max'], 'Inter-Regular', 40, W / 2, H * .25, alpha=230)
    D.text('Fakta', ['1 mm thin  \u00b7  37 N52 magnets  \u00b7  MagSafe & Qi2'], 'Inter-Regular', 34, W / 2, H * .74, alpha=220)
    D.logo(200, W / 2, H * .91)
    return D, 42, '51-variant-liggande-rad-mork'

def r52():  # ref 39, tre liggande skal på varm gradient
    bg = bg_fit(src('r39mac').convert('RGB'), 1080, 1080); D = d.Design(bg, 'L'); W, H = D.W, D.H; m = W * .07
    D.ink = (30, 30, 32)
    D.logo(230, m, H * .085, just='left')
    hoger(D, 'RD CASE V4', 'Poppins-SemiBold', 40, W - m, H * .07, namn='Rubrik')
    hoger(D, '1 mm thin. 37 N52 magnets.', 'Poppins-Regular', 40, W - m, H * .118, namn='Underrad 1')
    hoger(D, 'MagSafe & Qi2 ready.', 'Poppins-Regular', 40, W - m, H * .166, namn='Underrad 2')
    D.text('Nyhet', ['NEW FOR', 'IPHONE 18 PRO MAX'], 'Poppins-Bold', 56, m, H * .855, just='left', radavst=1.0)
    return D, 39, '52-tre-skal-liggande-varm'

def r53():  # ref 39, variant: svart främst, kall blågrå gradient
    bg = bg_fit(src('r39macB').convert('RGB'), 1080, 1080); D = d.Design(bg, 'L'); W, H = D.W, D.H; m = W * .07
    D.ink = (22, 26, 34)
    D.logo(230, m, H * .085, just='left')
    hoger(D, 'RD CASE V4', 'Poppins-SemiBold', 40, W - m, H * .07, namn='Rubrik')
    hoger(D, 'Three colors.', 'Poppins-Regular', 40, W - m, H * .118, namn='Underrad 1')
    hoger(D, 'Same 1 mm feel.', 'Poppins-Regular', 40, W - m, H * .166, namn='Underrad 2')
    D.text('Nyhet', ['NEW FOR', 'IPHONE 18 PRO MAX'], 'Poppins-Bold', 56, m, H * .855, just='left', radavst=1.0)
    return D, 39, '53-variant-tre-liggande-kall'

def r54():  # ref 37, tre skal ovanifrån i olika vinklar
    bg = bg_fit(src('r37mac').convert('RGB'), 1080, 1080); D = d.Design(bg, 'L'); W, H = D.W, D.H; m = W * .06
    D.ink = (24, 24, 26)
    D.logo(220, m, H * .085, just='left')
    D.text('Nyhet', ['NEW FOR', 'IPHONE 18 PRO MAX'], 'Poppins-Bold', 46, m, H * .87, just='left', radavst=1.0)
    hoger(D, 'RD CASE V4', 'Poppins-SemiBold', 38, W - m, H * .868, namn='Rubrik')
    hoger(D, '1 mm thin.', 'Poppins-Regular', 36, W - m, H * .912, namn='Underrad 1')
    hoger(D, '37 N52 magnets.', 'Poppins-Regular', 36, W - m, H * .954, namn='Underrad 2')
    return D, 37, '54-tre-skal-ovanifran'

# ---- NYA ANNONSER LÄGGS IN OVANFÖR DENNA RAD ----
if __name__ == '__main__':
    for a in sys.argv[1:]:
        try:
            D, rn, namn = globals()[a](); v = spara(D, namn); jamfor(rn, v, namn); print('KLAR', namn)
        except Exception:
            import traceback; traceback.print_exc()
