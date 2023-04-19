# -*- coding: shift_jis -*-
# xbasip sample programs
# nozwas <https://github.com/nozwas>

r"""sample06.py
    tgraphモジュールの使用例
"""

from xbasip.console import *
from xbasip.tgraph import *

width(64)
console(0, 32, 0)
cursor_off()

pal = ((0, 0, 0), (0, 31, 31), (31,31, 0), (31, 31, 31),
       (0, 0, 0), (0, 0, 31), (31, 0, 0), (31, 0, 31),
       (0, 0, 0), (0, 31, 0), (31, 12, 12), (27, 27, 17),
       (0, 0, 0), (8, 12, 31), (27, 8, 21), (21, 21, 21))
for i, c in enumerate(pal):
    t_palet(i, rgb(c[0], c[1], c[2]))

for j in range(4):
    locate(0, j * 8 + 1)
    print(f"テキストプレーン: 0b{j:02b}00", end="")
    for k in range(4):
        t_fill(256, j * 128 + k * 32,
               511, j * 128 + k * 32 + 31, j * 4 + k)
        t_fill(0, j * 128 + 1 * 32,
               255, j * 128 + 3 * 32 + 31, j * 4)
        if k > 0:
            color(k)
            print("")
            print(f"  COLOR({k})")
            print("  父のパソコンを超えろ。X68000", end="")

keyflush()
inkey()
t_cls()
width(96)
end()
