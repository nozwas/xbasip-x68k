# -*- coding: shift_jis -*-
# xbasip sample programs
# nozwas <https://github.com/nozwas>

r"""sample05.py
    mouseモジュール、stickモジュールの使用例
"""

from xbasip.console import *
from xbasip.mouse import *
from xbasip.stick import *
from binascii import unhexlify

K_RETURN, K_ESCAPE, K_SPACE, K_BACKSPACE = 0x0d, 0x1b, 0x20, 0x08
K_UP, K_LEFT, K_RIGHT, K_DOWN = 0x10, 0x02, 0x06, 0x0e
for i, code in enumerate((K_UP, K_LEFT, K_RIGHT, K_DOWN), start=25):
    key(i, chr(code).encode())
# カーソルキーは一時的に再定義（end()で復帰）

screen(0,0,1,1)
cursor_off()
mouse(4) # 初期化（ソフトキー無し）
mouse(1) # マウス表示オン
setmspos(128, 128)
msarea(0, 30, 255, 256 - 30)
deffont(0xec40, unhexlify("0ff03ffc7ffefffff3cff3cff3cfffff"
                          "ffff7ffe066006600e701c38f81ff00f"))
deffont(0xec41, unhexlify("0ff03ffc7ffefffff3cff3cff3cfffff"
                          "ffff7ffe0c303c3c781e60067e7e3e7c"))
print("矢印Key、JoyPAD、マウス左で操作")
print("ESCまたはトリガ、マウス右で終了")

x, y = 16, 8
xx, yy = 16, 7

while True:
    k = inkey(0)
    if k != 0:
        keyflush() # キーバッファのクリア
    s = stick(1)
    b = strig(1)
    p = mspos()
    m = msstat()
    locate(0, 15)
    color(1)
    print(f"({p[0]:>3},{p[1]:>3})", end="")
    if m[2]:
        if p[0] // 8 < x:
            xx = x - 1
        if p[0] // 8 > x:
            xx = x + 1
        if p[1] // 16 < y:
            yy = y - 1
        if p[1] // 16 > y:
            yy = y + 1    

    if k == K_LEFT or s in (1, 4, 7):
        xx = x - 1
    if k == K_RIGHT or s in (3, 6, 9):
        xx = x + 1
    if k == K_UP or s in (7, 8, 9):
        yy = y - 1
    if k == K_DOWN or s in (1, 2, 3):
        yy = y + 1
    if xx < 0 or xx > 30:
        xx = x
    if yy < 2 or yy > 14:
        yy = y
    if xx != x or yy != y:
        locate(x, y)
        print("  ", end="")
        x, y = xx, yy
        color(y % 3 + 1)
        locate(x, y)
        print("\uec40" if x & 1 else "\uec41", end="")

    if k == K_ESCAPE or b > 0 or m[3]:
        break

mouse(2) # マウス表示オフ
width(96)
end()
