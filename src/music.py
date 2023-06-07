# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""music.py
    Music module, a part of xbasip package
"""

import x68k
from ustruct import pack

def m_init(mode=0):
    opmdrv = x68k.iocs(x68k.i.B_LPEEK, a1=(0x000400 + 4 * 0xf0))
    if opmdrv < 0 or (opmdrv >= 0xfe0000 and opmdrv <= 0xffffff):
        raise RuntimeError("OPMDRV is not installed")
    x68k.iocs(x68k.i.OPMDRV, d1=0x00, d2=mode)
    for i in range(1000):
        pass

def m_alloc(trk, size):
    x68k.iocs(x68k.i.OPMDRV, d1=0x01, d2=(trk << 16) | size)

def m_free(trk):
    return x68k.iocs(x68k.i.OPMDRV, d1=0x07, d2=trk)

def m_assign(ch, trk):
    x68k.iocs(x68k.i.OPMDRV, d1=0x02, d2=(ch << 16) | trk)

def m_play(*ch_s):
    d2 = d3 = d4 = 0
    for ch in ch_s:
        d2 |= (1 << (ch - 1)) if ch >= 1 and ch <= 32 else 0
        d3 |= (1 << (ch - 33)) if ch >= 33 and ch <= 64 else 0
        d4 |= (1 << (ch - 65)) if ch >= 65 and ch <= 80 else 0
    x68k.iocs(x68k.i.OPMDRV, d1=0x08, 
              d2=pack('L', d2), d3=pack('L', d3), d4=pack('L', d4))

def m_stop(*ch_s):
    d2 = d3 = d4 = 0
    for ch in ch_s:
        d2 |= (1 << (ch - 1)) if ch >= 1 and ch <= 32 else 0
        d3 |= (1 << (ch - 33)) if ch >= 33 and ch <= 64 else 0
        d4 |= (1 << (ch - 65)) if ch >= 65 and ch <= 80 else 0
    x68k.iocs(x68k.i.OPMDRV, d1=0x0a,
              d2=pack('L', d2), d3=pack('L', d3), d4=pack('L', d4))

def m_cont(*ch_s):
    d2 = d3 = d4 = 0
    for ch in ch_s:
        d2 |= (1 << (ch - 1)) if ch >= 1 and ch <= 32 else 0
        d3 |= (1 << (ch - 33)) if ch >= 33 and ch <= 64 else 0
        d4 |= (1 << (ch - 65)) if ch >= 65 and ch <= 80 else 0
    x68k.iocs(x68k.i.OPMDRV, d1=0x0b,
              d2=pack('L', d2), d3=pack('L', d3), d4=pack('L', d4))

def m_stat(ch=0):
    stat =  x68k.iocs(x68k.i.OPMDRV, d1=0x09, d2=0, d3=0, d4=0)
    return stat if ch <= 0 or ch > 32 else 1 if stat & (1 << (ch - 1)) else 0 

def m_tempo(tempo):
    x68k.iocs(x68k.i.OPMDRV, d1=0x05, d2=tempo)

def m_trk(trk, mml):
    mml += "\x00"
    err = x68k.iocs(x68k.i.OPMDRV, d1=0x06, d2=trk, a1=mml)
    if err == 28:
        raise RuntimeError("trk buffer is too small")
    elif err != 0:
        raise RuntimeError("wrong mml data")
    
def m_vset(vo, buf):
    x68k.iocs(x68k.i.OPMDRV, d1=0x04, d2=vo, a1=buf)

def m_vget(vo, buf=None):
    if buf is None:
        buf = bytearray(5*11)
    x68k.iocs(x68k.i.OPMDRV, d1=0x03, d2=vo, a1w=buf)
    return buf

def m_atoi(trk):
    return x68k.iocs(x68k.i.OPMDRV, d1=0x0c, d2=trk)

