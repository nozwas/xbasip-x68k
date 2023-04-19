# -*- coding: shift_jis -*-
# xbasip sample programs
# nozwas <https://github.com/nozwas>

r"""sample03.py
    spriteモジュールの使用例
"""
from xbasip.console import *
from xbasip.sprite import *
from random import randrange
from math import pi, sin, cos
from binascii import unhexlify
              
PAT0 = ("0000000044400000"
        "0000000444000000"
        "0000000400000000"
        "0002222402222000"
        "0222222222222200"
        "2222272222222220"
        "2222227772222222"
        "2222222222222222"
        "2222222222222222"
        "2222222222222222"
        "2222222222222222"
        "2222222222222622"
        "0222222222226620"
        "0222222222266220"
        "0022222226662200"
        "0000222222220000")
              
PAT1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0,
        0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0,
        0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 3, 3, 3, 3, 0, 0,
        3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0,
        3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3,
        3, 3, 7, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2,
        3, 3, 3, 7, 3, 3, 2, 2, 3, 3, 7, 3, 3, 3, 3, 2,
        0, 3, 3, 3, 3, 2, 2, 0, 3, 3, 3, 7, 3, 3, 2, 2,
        0, 0, 3, 3, 2, 2, 0, 0, 0, 3, 3, 3, 3, 2, 2, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0]
              
PAT2 = [ 0 ] * 64

PAT3 = [2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 0, 2, 2, 2, 2,
        2, 2, 2, 0, 2, 2, 2, 2,
        2, 2, 2, 0, 2, 2, 2, 2,
        0, 2, 2, 0, 2, 2, 0, 2,
        2, 0, 2, 0, 2, 0, 2, 2,
        2, 2, 0, 0, 0, 2, 2, 2,
        2, 2, 2, 0, 2, 2, 2, 2]

PAT4 = ("00010000"
        "00100000"
        "01000000"
        "11111110"
        "01000000"
        "00100000"
        "00010000"
        "00000000")

def array2pat(a):
    return bytes([(x << 4) | y for x, y in zip(a[0::2], a[1::2])])

screen(0,3,1,1)
key_off()
cursor_off()

sp_init()
sp_clr(0, 255)
sp_disp(1)
sp_on(0, 1)

sp_def(0, unhexlify(PAT0), 1) # 16x16 文字列から
sp_def(1, array2pat(PAT1), 1) # 16x16 整数配列から
sp_def(8, array2pat(PAT2), 0) # 8x8 整数配列から
sp_def(9, array2pat(PAT3), 0) # 8x8 整数配列から
sp_def(10, unhexlify(PAT4), 0) # 8x8 文字列から

sp_color(1, rgb(24, 24, 24)) # pal_blk = 1(default) for BG
sp_color(2, rgb(0, 0, 15))

sp_color(2, rgb(31, 0, 0), 2) # pal_blk = 2 for SP
sp_color(3, rgb(31, 0, 31), 2)
sp_color(4, rgb(0, 31, 0), 2)
sp_color(6, rgb(31, 31, 0), 2)
sp_color(7, rgb(31, 31, 31), 2)

bg_fill(0, sp_code(8, 0, 0, 1))
bg_fill(1, sp_code(9, 0, 1, 1)) # v reverse
bg_set(0, 0, 1)
bg_set(1, 1, 1)
for i in range(300):
    bg_put(0, randrange(64), randrange(64),
           sp_code(10, 0, 0, 1))

x1 = y1 = 0
t, dt = 0, 1

keyflush()

while True:
    if inkey0() != 0:
        break
    x1 = 0 if x1 == 511 else (x1 + 1)
    y1 = 0 if y1 == 511 else (y1 + 1)
    bg_scroll(0, x1, 0)
    bg_scroll(1, 0, y1)
    t += dt
    if t == 0 or t == 272:
        dt = - dt
    f = (pi * 2 * t) / 272 * 8
    x2 = int(128 - 120 * sin(f) * cos(f) * sin(f + pi / 2))
    sp_set(0, x2, t, sp_code(0, 0, 0, 2), 3)
    sp_set(1, t, x2, sp_code(1, 1, 0, 2), 2) # h reverse    
    x68k.vsync()

width(96)
end()
