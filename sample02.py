# -*- coding: shift_jis -*-
# xbasip sample programs
# nozwas <https://github.com/nozwas>

r"""sample02.py
    graphモジュールの使用例
"""
from xbasip.console import *
from xbasip.graph import *
from random import randrange

#screen(2, 0, 1, 1) # 768x512dots  16colors 1pages
#screen(1, 3, 1, 1) # 512x512dots 64Kcolors 1pages
#screen(1, 2, 1, 1) # 512x512dots 256colors 2pages
#screen(1, 1, 1, 1) # 512x512dots  16colors 4pages
#screen(0, 3, 1, 1) # 256x256dots 64Kcolors 1pages
#screen(0, 2, 1, 1) # 256x256dots 256colors 2pages
#screen(0, 1, 1, 1) # 256x256dots  16colors 4pages

screen(2, 0, 1, 1) # 768x512dots  16colors 1pages
key_off() # funckey disp off
for i in range(100):
    x, y, r = randrange(768), randrange(512), randrange(200)
    c = i % 16
    circle(x, y, r, c, 0, 360, 256)

screen(1, 2, 1, 1) # 512x512dots 256colors 2pages
key_off() # funckey disp off
for i in range(100):
    x1, y1 = randrange(512), randrange(512)
    x2, y2 = randrange(512), randrange(512)
    c = randrange(256)
    style = randrange(65536)
    line(x1, y1, x2, y2, c, style)

screen(0, 3, 1, 1) # 256x256dots 64Kcolors 1pages
for i in range(100):
    x1, y1 = randrange(256), randrange(256)
    x2, y2 = randrange(256), randrange(256)
    c = randrange(65536)
    style = randrange(65536)
    r = randrange(2)
    if r == 1:
        box(x1, y1, x2, y2, c, style)
    else:
        fill(x1, y1, x2, y2, c)

screen(1, 3, 1, 1) # 512x512dots 64Kcolors 1pages
key_off() # funckey disp off
for v in range(31, 0, -2):
    circle(128, 128, v * 4, hsv(0, 31, v), 0, 360, 256)
    paint(128, 128, hsv(0, 31, v))
    circle(384, 384, v * 4, hsv(96, 31, v), 0, 360, 256)
    paint(384, 384, hsv(96, 31, v))
for mag in range(1, 11):
    symbol(256, 256, "X68", mag, mag, 2, randrange(65536), mag % 4)
for lv in reversed(range(16)):
    contrast(lv)
    x68k.vsync()
    x68k.vsync()
    x68k.vsync()

width(96)
end()
