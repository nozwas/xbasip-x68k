# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""mouse.py
    Mouse module, a part of xbasip package
"""

import x68k

def mouse(cmd=0):
    if cmd == 0: # INIT(softkey auto)
        x68k.iocs(x68k.i.MS_INIT)
        x68k.iocs(x68k.i.SKEY_MOD, d1=-1)
    elif cmd == 1: # CUR ON
        x68k.iocs(x68k.i.MS_CURON)
    elif cmd == 2: # CUR OFF
        x68k.iocs(x68k.i.MS_CUROF)
    elif cmd == 3: # CUR STAT
        return x68k.iocs(x68k.i.MS_STAT) != 0
    elif cmd == 4: # INIT(softkey off)
        x68k.iocs(x68k.i.MS_INIT)
        x68k.iocs(x68k.i.SKEY_MOD, d1=0)

def msarea(x1, y1, x2, y2):
    x68k.iocs(x68k.i.MS_LIMIT, d1=(x1 << 16) | y1, d2=(x2 << 16) | y2)

def setmspos(x, y):
    x68k.iocs(x68k.i.MS_CURST, d1=(x << 16) | y)

def mspos():
    pos = x68k.iocs(x68k.i.MS_CURGT)
    return ((pos >> 16) & 0xffff, pos & 0xffff)

def msstat():
    # (x, y, btn_l, btn_r)
    stat = x68k.iocs(x68k.i.MS_GETDT)
    x = (stat >> 24) & 0xff
    y = (stat >> 16) & 0xff
    l = (stat >> 8) & 1
    r = stat & 1
    return (x if x < 128 else (x - 256), y if y < 128 else (y - 256),
            l == 1, r == 1)

def msbtn(wait_push=True, btn=0, time=0):
    # btn: 0=left, 1=right, time: wait time
    if wait_push:
        return x68k.iocs(x68k.i.MS_ONTM, d1=0 if btn == 0 else -1, d2=time)
    else: # wait_release
        return x68k.iocs(x68k.i.MS_OFFTM, d1=0 if btn == 0 else -1, d2=time)

