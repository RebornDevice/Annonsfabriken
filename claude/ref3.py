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

# ---- NYA ANNONSER LÄGGS IN OVANFÖR DENNA RAD ----
if __name__ == '__main__':
    for a in sys.argv[1:]:
        try:
            D, rn, namn = globals()[a](); v = spara(D, namn); jamfor(rn, v, namn); print('KLAR', namn)
        except Exception:
            import traceback; traceback.print_exc()
