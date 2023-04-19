# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""tgraph.py
    Text Graphic module, a part of xbasip package
"""

import x68k
from struct import pack

_t_last_point = [0, 0]

def t_cls(graph=False):
    x68k.iocs(x68k.i.TXFILL, a1=pack('6h', 0x800f, 0, 0, 1024, 1024, 0))
    if graph:
        x68k.iocs(x68k.i.WIPE)

def t_scroll(x, y):
    x68k.iocs(x68k.i.SCROLL, d1=8, d2=x, d3=y)

def t_pset(x, y, color_bit):
    global _t_last_point
    x68k.iocs(x68k.i.TXLINE, a1=pack('6h', color_bit | 0x8000, x, y,
                                     1, 1, 0xff))
    _t_last_point = (x, y)

def t_line(x1, y1, x2, y2, color_bit, style=0xff):
    global _t_last_point
    x68k.iocs(x68k.i.TXLINE, a1=pack('6h', color_bit | 0x8000, x1, y1,
                                     x2 - x1 + 1, y2 - y1 + 1, style))
    _t_last_point = (x2, y2)

def t_line_to(x, y, color_bit, style=0xff):
    x1, y1 = _t_last_point
    t_line(x1, y1, x, y, color_bit, style)

def t_box(x1, y1, x2, y2, color_bit, style=0xff):
    x68k.iocs(x68k.i.TXBOX, a1=pack('6h', color_bit | 0x8000, x1, y1,
                                    x2 - x1 + 1, y2 - y1 + 1, style))

def t_fill(x1, y1, x2, y2, color_bit, style=0xffff):
    x68k.iocs(x68k.i.TXFILL, a1=pack('6h', color_bit | 0x8000, x1, y1,
                                     x2 - x1 + 1, y2 - y1 + 1, style))

def t_palet(pal=None, color=None):
    # same to tpalet2
    if color is None:
        if pal is None:
            for pal in range(16):
                x68k.iocs(x68k.i.TPALET, d1=pal, d2=-2)
        else:
            return x68k.iocs(x68k.i.TPALET2, d1=pal, d2=-1)
    else:
        x68k.iocs(x68k.i.TPALET2 ,d1=pal, d2=color)

