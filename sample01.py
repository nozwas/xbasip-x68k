# -*- coding: shift_jis -*-
# xbasip sample programs
# nozwas <https://github.com/nozwas>

r"""sample01.py
    console���W���[���̎g�p��
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
print("�����L�[�������Ă�������")
print("-" * 50, end="")
keyflush() # �L�[�o�b�t�@���N���A
k = inkey() # inkey()�͓��͂����܂ő҂��܂�

width(96)
console(0, 31, 0)
cls()

beep()
print("������x�����L�[�������Ă�������")
print("-" * 50, end="")

keyflush()
while inkey0() == 0: #inkey0()�͓��͂�҂��܂���
    color(randrange(16))
    locate(randrange(96), randrange(28) + 2)
    print("X68K", end="")

color(3)
cls()
end()
