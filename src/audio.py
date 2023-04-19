# -*- coding: shift_jis -*-
# xbasip: X-BASIC like Python package for micropython-x68k
# nozwas <https://github.com/nozwas>

r"""audio.py
    Audio module, a part of xbasip package
"""

import x68k

def a_play(buf, freq, ch_bit=0b11, l=0):
    l = len(buf) if l == 0 else l
    x68k.iocs(x68k.i.ADPCMOUT, d1=(freq  << 8) | ch_bit, d2=l, a1=buf)

def a_rec(buf, freq, l=0):
    l = len(buf) if l == 0 else l
    x68k.iocs(x68k.i.ADPCMINP, d1=(freq << 8) | 3, d2=l, a1w=buf)
    return buf

def a_stat():
    return x68k.iocs(x68k.i.ADPCMSNS)

def a_end():
    x68k.iocs(x68k.i.ADPCMMOD, d1=0)

def a_stop():
    x68k.iocs(x68k.i.ADPCMMOD, d1=1)

def a_cont():
    x68k.iocs(x68k.i.ADPCMMOD, d1=2)
