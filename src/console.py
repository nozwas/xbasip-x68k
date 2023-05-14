# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""console.py
    Console module, a part of xbasip package
"""

import x68k
from uctypes import addressof
from ustruct import pack
from usys import exit

_initial_fkey_disp = None
_initial_fkey_str = None
_initial_font_pat = []

def screen(disp_size, page_mode, res=1, disp_on=True):
    disp_size = ((256, 256), (512, 512), (768, 512))[disp_size]
    page_size = (1024, 512, 512, 512)[page_mode]
    colors = (16, 16, 256, 65536)[page_mode]
    pages = (1, 4, 2, 1)[page_mode]
    crtmod = ((1024, 512, 16, 1), (1024, 256, 16, 1), (512, 512, 16, 4),
              (512, 256, 16, 4), (512, 512, 256, 2), (512, 256, 256, 2),
              (512, 512, 65536, 1), (512, 256, 65536, 1), (1024, 768, 16, 1))
    m = 999
    for i in range(9):
        if crtmod[i][0] == page_size and crtmod[i][1] == disp_size[0] \
           and crtmod[i][2] == colors and crtmod[i][3] == pages:
            m = i * 2 + 1 - res
            break
    if m <= 16:
        _backup_fkey_disp()
        x68k.iocs(x68k.i.CRTMOD, d1=m)
        if disp_size[0] in (512, 768):
            console(0, 31, 1)
    else:
        raise RuntimeError("wrong parameter")
    if disp_on:
        x68k.iocs(x68k.i.G_CLR_ON)
    cls()

def width(columns):
    if columns == 96:
        screen(2, 0, res=1, disp_on=False)
    elif columns == 64:
        screen(1, 0, res=1, disp_on=False)
    else:
        raise RuntimeError("wrong parameter")

def console(start, lines, fkey):
    if fkey:
        key_on()
    else:
        key_off()
    x68k.dos(x68k.d.CONCTRL, pack('3h', 15, start, lines))

def cls(all_clear=False):
    x68k.iocs(x68k.i.B_CLR_ST, d1=2)
    if all_clear:
        x68k.iocs(x68k.i.WIPE)
        x68k.iocs(x68k.i.TXFILL, a1=pack('6h', 0x800f, 0, 0, 1024, 1024, 0))
        x68k.iocs(x68k.i.BGCTRLST, d1=0, d2=0, d3=0)        
        x68k.iocs(x68k.i.BGCTRLST, d1=1, d2=1, d3=0)        
        x68k.iocs(x68k.i.SP_OFF)

@micropython.native
def locate(x, y, cursor=None):
    if cursor is not None:
        if cursor:
            cursor_on()
        else:
            cursor_off()
    x68k.iocs(x68k.i.B_LOCATE, d1=x, d2=y)

def pos():
    return (x68k.iocs(x68k.i.B_LOCATE, d1=-1) >> 16) & 0xffff

def csrlin():
    return x68k.iocs(x68k.i.B_LOCATE, d1=-1) & 0xffff

@micropython.native
def color(pal): # pal: 0=black, 1=cyan, 2=yellow, 3=white
    x68k.iocs(x68k.i.B_COLOR, d1=pal)

def tpalet(pal=None, color=None):
    if color is None:
        if pal is None:
            for pal in range(16):
                x68k.iocs(x68k.i.TPALET, d1=pal, d2=-2)
        else:
            return x68k.iocs(x68k.i.TPALET, d1=pal, d2=-1)
    else:
        x68k.iocs(x68k.i.TPALET, d1=pal, d2=color)

def tpalet2(pal=None, color=None):
    if color is None:
        if pal is None:
            for pal in range(16):
                x68k.iocs(x68k.i.TPALET2, d1=pal, d2=-2)
        else:
            return x68k.iocs(x68k.i.TPALET2, d1=pal, d2=-1)
    else:
        x68k.iocs(x68k.i.TPALET2, d1=pal, d2=color)

def inkey(wait=True):
    if wait:
        return x68k.dos(x68k.d.GETC)
    else:
        return x68k.dos(x68k.d.INPOUT, b'\x00\xff')

def inkeyS(wait=True):
    s = inkey(wait)
    return "" if s == 0 else chr(s)

@micropython.native
def inkey0():
    return x68k.dos(x68k.d.INPOUT, b'\x00\xff')

@micropython.native
def keyinp():
    return x68k.iocs(x68k.i.B_KEYINP)

@micropython.native
def keysns():
    return x68k.iocs(x68k.i.B_KEYSNS)

@micropython.native
def sftsns():
    return x68k.iocs(x68k.i.B_SFTSNS)

@micropython.native
def bitsns(group):
    return x68k.iocs(x68k.i.BITSNS, d1=group)

@micropython.native
def keyflush():
    x68k.dos(x68k.d.KFLUSH, b'\x00\x06\x00\xfe')

def _backup_fkey_str():
    global _initial_fkey_str
    if _initial_fkey_str is None:
        _initial_fkey_str = bytearray(712)
        x68k.dos(x68k.d.FNCKEY, pack('hl', 0, addressof(_initial_fkey_str)))

def key(fn, buf=None):
    if buf is None:
        buf = bytearray(712 if fn == 0 else 32 if fn < 21 else 6)
        x68k.dos(x68k.d.FNCKEY, pack('hl', fn, addressof(buf)))
        return buf
    else:
        _backup_fkey_str()
        buf += "\x00"
        x68k.dos(x68k.d.FNCKEY, pack('hl', 0x100 | fn, addressof(buf)))    
        
def _backup_fkey_disp():
    global _initial_fkey_disp
    if _initial_fkey_disp is None:
        _initial_fkey_disp = x68k.dos(x68k.d.CONCTRL, pack('2h', 14, -1))

def key_on():
    _backup_fkey_disp()
    x68k.dos(x68k.d.CONCTRL, pack('2h', 14, 0))

def key_off():
    _backup_fkey_disp()
    x68k.dos(x68k.d.CONCTRL, pack('2h', 14, 3))

def cursor_on():
    x68k.iocs(x68k.i.OS_CURON)

def cursor_off():
    x68k.iocs(x68k.i.OS_CUROF)

def deffont(code, buf, font_size=1):
    global _initial_font_pat
    # code: KANJI 0xeb9f-0xebfc, 0xec40-0xec7e, ANK 0xf400-0xf5ff
    # font_size: 1..8x16/16x16, 2..12x24/24x24
    if font_size in (0, 1, 2):
        font_size = (6, 8, 12)[font_size]
    _initial_font_pat.append((code, getfont(code)))
    x68k.iocs(x68k.i.DEFCHR, d1=(font_size << 16) | code, a1=buf)

def getfont(code, buf=None, font_size=1):
    # font_size: 0..6x12/12x12, 1..8x16/16x16, 2..12x24/24x24
    if font_size in (0, 1, 2):
        font_size = (6, 8, 12)[font_size]
    if buf is None:
        buf = bytearray((4 + 72) if font_size == 12 else (4 + 4 * font_size))
    elif len(buf) < (4 + 72) if font_size == 12 else (4 + 4 * font_size):
        raise RuntimeError("wrong buf size")
    x68k.iocs(x68k.i.FNTGET, d1=(font_size << 16) | code, a1w=buf)
    return buf[1], buf[3], buf[4:]
    
@micropython.native
def beep():
    x68k.dos(x68k.d.INPOUT, b'\x00\x07')

def end(arg=None):
    if _initial_fkey_str is not None:
        x68k.dos(x68k.d.FNCKEY, pack('hl', 0x100,
                                     addressof(_initial_fkey_str)))    
    if _initial_fkey_disp is not None:
        x68k.dos(x68k.d.CONCTRL, pack('2h', 14, _initial_fkey_disp))
    for p in _initial_font_pat:
        x68k.iocs(x68k.i.DEFCHR, d1=((p[1][1] // 2) << 16) | p[0], a1=p[1][2])
    cursor_on()
    tpalet()
    if type(arg) is int or arg is None:
        exit(arg)
    else:
        print(arg)
        exit(1)

def priority(sp, tx, gr):
    l = [sp, tx, gr]
    if sum(l) != 3 or min(l) != 0 or max(l) != 2:
        raise RuntimeError("wrong parameter")
    g = x68k.iocs(x68k.i.PRIORITY, d1=-1) & 0xff
    x68k.iocs(x68k.i.PRIORITY, d1=(sp << 12) | (tx << 10) | (gr << 8) | g)

def crtmod(mode, disp_on=True):
    _backup_fkey_disp()
    x68k.iocs(x68k.i.CRTMOD, d1=mode)
    if disp_on:
        x68k.iocs(x68k.i.G_CLR_ON)
