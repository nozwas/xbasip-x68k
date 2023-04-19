# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""stick.py
    Joy Stick module, a part of xbasip package
"""

import x68k

def stick(joy=1):
    if joy < 1 or joy > 2:
        raise RuntimeError("wrong parameter")
    js = x68k.iocs(x68k.i.JOYGET, d1=joy-1)
    js = ~js if js else 0
    return ((0, 4, 6),(8, 7, 9),(2, 1, 3))[js & 3][(js >> 2) & 3]

def strig(joy=1):
    if joy < 1 or joy > 2:
        raise RuntimeError("wrong parameter")
    js = x68k.iocs(x68k.i.JOYGET, d1=joy-1)
    js = ~js if js else 0
    return (js >> 5) & 3
