# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""sprite.py
    Sprite module, a part of xbasip package
"""

import x68k
from struct import pack

_sprite_obj = x68k.Sprite()

def bg_set(bg, page, disp_on=True):
    x68k.iocs(x68k.i.BGCTRLST, d1=bg, d2=page, d3=int(disp_on))

@micropython.native
def bg_scroll(bg, x, y, vsync=0):
    x68k.iocs(x68k.i.BGSCRLST,
              d1=pack('L', (vsync << 31) | bg), d2=x, d3=y)

def bg_stat(bg):
    # returns: (x, y, page, disp_on)
    scrl = x68k.iocs(x68k.i.BGSCRLGT, d1=bg, rd=3)
    ctrl = x68k.iocs(x68k.i.BGCTRLGT, d1=bg)
    return (scrl[2], scrl[3], int(ctrl > 1),  (ctrl & 1) == 1)

def bg_fill(page, code):
    x68k.iocs(x68k.i.BGTEXTCL, d1=page, d2=code)

def bg_get(page, x, y):
    return x68k.iocs(x68k.i.BGTEXTGT, d1=page, d2=x, d3=y)

@micropython.native
def bg_put(page, x, y, code):
    _sprite_obj.bgput(0, x, y, code)

def sp_init():
    x68k.iocs(x68k.i.SP_INIT)

def sp_clr(code1=None, code2=None):
    # pat clear
    if type(code1) is not tuple:
        if code1 is None:
            code1, code2 = 0, 255 if code2 is None else code2
        else:
            code2 = code1 if code2 is None else code2
        code1 = tuple(range(code1, code2 + 1))
    for code in code1:
        x68k.iocs(x68k.i.SP_CGCLR, d1=code)

def sp_color(pal, color, pal_blk=1, vsync=0):
    return x68k.iocs(x68k.i.SPALET,
                     d1=pack('L', (vsync << 31) | pal),
                     d2=pal_blk, d3=color)

def sp_on(sp1=None, sp2=None, prio=3, vsync=0):
    if type(sp1) is not tuple:
        if sp1 is None:
            sp1, sp2 = 0, 127 if sp2 is None else sp2
        else:
            sp2 = sp1 if sp2 is None else sp2
        sp1 = tuple(range(sp1, sp2 + 1))
    for sp in sp1:
        x68k.iocs(x68k.i.SP_REGST,
                  d1=pack('L', (vsync << 31) | sp),
                  d2=-1,  d3=-1, d4=-1, d5=prio)

def sp_off(sp1=None, sp2=None, vsync=0):
    sp_on(sp1, sp2, 0, vsync)

def sp_def(code, buf, pat_size=1):
    # pat_size: 0..8x8, 1..16x16, 2..16x16(IOCS order)
    _sprite_obj.defcg(code, buf, pat_size)

def sp_pat(code, pat_size=1):
    # pat_size: 0..8x8, 1..16x16
    buf = bytearray(32 if pat_size == 0 else 128)
    x68k.iocs(x68k.i.SP_GTPCG, d1=code, d2=pat_size, a1w=buf)
    return buf

@micropython.native
def sp_move(sp, x, y, code, vsync=0):
    _sprite_obj.set(sp, x, y, code, 3, vsync)

@micropython.native
def sp_set(sp, x, y, code, prio, vsync=0):
    _sprite_obj.set(sp, x, y, code, prio, vsync)

def sp_disp(disp_on=True):
    if disp_on:
        x68k.iocs(x68k.i.SP_ON)
    else:
        x68k.iocs(x68k.i.SP_OFF)

def sp_stat(sp):
    #returns: x, y, code=pal_blk|h_rev|v_rev|code, prio
    d = x68k.iocs(x68k.i.SP_REGGT, d1=sp, rd=5)
    return (d[2], d[3], d[4], d[5])

def sp_code(code, hrev, vrev, pal_blk):
    return code | (vrev << 15) | (hrev << 14) | (pal_blk << 8)
