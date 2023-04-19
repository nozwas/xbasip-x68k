# -*- coding: shift_jis -*-
# xbasip sample programs
# nozwas <https://github.com/nozwas>

r"""sample01.py
    consoleモジュールの使用例
"""
from xbasip.console import *
from random import randrange

width(64)
console(0, 31, 0)
color(2)
cursor_off()

for i in range(100):
    print("personal workstation X68000   ", end = "")

console(5, 21, 0)
cls()

for i in range(200):
    color(1)
    print("personal workstation X68000   ", end = "")

color(3)
print("")
print("-" * 50)
print("何かキーを押してください")
print("-" * 50, end="")
keyflush() # キーバッファをクリア
k = inkey() # inkey()は入力されるまで待ちます

width(96)
console(0, 31, 0)
cls()

beep()
print("もう一度何かキーを押してください")
print("-" * 50, end="")

keyflush()
while inkey0() == 0: #inkey0()は入力を待ちません
    color(randrange(16))
    locate(randrange(96), randrange(28) + 2)
    print("X68K", end="")

color(3)
cls()
end()
