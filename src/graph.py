# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""graph.py
    Graphic module, a part of xbasip package
"""

import x68k
from uctypes import addressof
from struct import pack, unpack

_last_point = [0, 0]

def crtmod(mode):
    global _last_point
    x68k.iocs(x68k.i.CRTMOD, d1=mode)
    _last_point = (0, 0)

def palet(pal, color):
    x68k.iocs(x68k.i.GPALET ,d1=pal, d2=color)

def rgb(r, g=None, b=None):
    if type(r) is tuple:
        return rgb(r[0], r[1], r[2])
    else:
        return (g << 11)  | (r << 6) | (b << 1)

def rgb24(r, g=None, b=None):
    if type(r) is tuple:
        return rgb24(r[0], r[1], r[2])
    else:
        return rgb(r >> 3, g >> 3, b >> 3)

def hsv(h, s=None, v=None):
    if type(h) is tuple:
        return hsv(h[0], h[1], h[2])
    else:
        return x68k.iocs(x68k.i.HSVTORGB, d1=(h << 16) | (s << 8) | v)

@micropython.native
def pset(x, y, color):
    global _last_point
    x68k.iocs(x68k.i.PSET, a1=pack('3h', x, y, color))
    _last_point = (x, y)

@micropython.native
def line(x1, y1, x2, y2, color, style=0xffff):
    global _last_point
    x68k.iocs(x68k.i.LINE, a1=pack('6h', x1, y1, x2, y2, color, style))
    _last_point = (x2, y2)

@micropython.native
def line_to(x, y, color, style=0xffff):
    x1, y1 = _last_point
    line(x1, y1, x, y, color, style)

def box(x1, y1, x2, y2, color, style=0xffff):
    x68k.iocs(x68k.i.BOX, a1=pack('6h', x1, y1, x2, y2, color, style))

def fill(x1, y1, x2, y2, color):
    x68k.iocs(x68k.i.FILL, a1=pack('5h',x1, y1, x2, y2, color))

def circle(x, y, r, color=None, start=0, end=360, ratio=256):
    x68k.iocs(x68k.i.CIRCLE,a1=pack('7h', x, y, r, color, start, end, ratio))

def paint(x, y, color, buf=None):
    if buf is None:
        buf = bytearray(1024)
    x68k.iocs(x68k.i.PAINT,
              a1=pack('3h2l', x, y, color,
                      addressof(buf), addressof(buf) + len(buf)))

def get(x1, y1, x2, y2, buf=None):
    depth = (4, 8, 16, 4)[x68k.iocs(x68k.i.G_MOD, d1=-1)]
    if buf is None:
        buf = bytearray(((x2-x1+1)*(y2-y1+1)*depth + 4) >> 3)
    x68k.iocs(x68k.i.GETGRM,
              a1=pack('4h2l', x1, y1, x2, y2,
                      addressof(buf), addressof(buf) + len(buf)))
    return buf

@micropython.native
def put(x1, y1, x2, y2, buf):
    x68k.iocs(x68k.i.PUTGRM,
              a1=pack('4h2l', x1, y1, x2, y2,
                      addressof(buf), addressof(buf) + len(buf)))

def symbol(x, y, str, xmag, ymag, font_size, color, dir=0):
    # font_size: 0=6*12, 1=8*16, 2=12*24, dir: 0=Right, 1=Up, 2=Left, 3=Down
    if font_size in (6, 8, 12):
        font_size = (0, 1, 2)[(6, 8, 12).index(font_size)]
    x68k.iocs(x68k.i.SYMBOL, a1=pack('2h1l2b1h2b', x, y, addressof(str),
                                     xmag, ymag, color, font_size, dir))

def point(x, y):
    p = pack('3h', x, y, 0)
    x68k.iocs(x68k.i.POINT, a1w=addressof(p))
    return unpack('3h', p)[2]

def contrast(level):
    return x68k.iocs(x68k.i.CONTRAST, d1=level)

def window(x1, y1, x2, y2):
    return x68k.iocs(x68k.i.WINDOW, d1=x1, d2=y1, d3=x2, d4=y2)

def wipe():
    global _last_point
    x68k.iocs(x68k.i.WIPE)
    _last_point = (0, 0)

def apage(page):
    x68k.iocs(x68k.i.APAGE, d1=page)

def vpage(page_bit):
    x68k.iocs(x68k.i.VPAGE, d1=page_bit)

def home(page, x, y):
    x68k.iocs(x68k.i.HOME, d1=1 << page, d2=x, d3=y)

@micropython.native
def scroll(page, x, y): # page: graph=0..3, text=8
    x68k.iocs(x68k.i.SCROLL, d1=page, d2=x, d3=y)
