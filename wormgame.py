# -*- coding: shift_jis -*-
# worm: xbasip demo game
# nozwas <https://github.com/nozwas>

r"""wormgame.py
    Control the worm so that it does not hit walls and itself. 
    Take all fruits to clear the stage.
"""

from xbasip.console import *
from xbasip.audio import *
from xbasip.tgraph import *
from xbasip.graph import rgb
from binascii import unhexlify
from random import randrange, seed
from time import time

GAME_SPEED = 3 # 0=fastest
GAME_CLEAR, STAGE_CLEAR, MISTAKE = 1, 2, 3


def print_at(x, y, s, c=None):
    if c is not None:
        color(c)
    locate(x, y)
    print(s, end="")


def print_message(x, y, message, c=None, spacing=0):
    for s in message:
        print_at(x, y, s, c)
        y += spacing + 1


def print_title(x, y, title, char="*", wchar=False):
    wc = 2 if wchar else 1
    for l in title:
        xx = x
        for c in l:
            if c != " ":
                print_at(xx, y, char, 0 if c == "." else int(c))
            xx += wc
        y += 1


def print_frame(x, y, w, h, char="++++-|", wchar=False, c=None):
    # char = 0:TopLeft + 1:TRight + 2:BotomL + 3:BR + 4:Helv + 5:Vert
    # ex. char = "++++-|"
    wc = 2 if wchar else 1
    print_at(x, y, char[0] + char[4] * (w - 2) + char[1], c)
    for y in range(y + 1, y + h -1):
        print_at(x, y, char[5], c)
        print_at(x + (w - 1) * wc, y, char[5], c)
    print_at(x, y + 1, char[2] + char[4] * (w - 2) + char[3], c)


def print_score():
    color(C_TEXT)
    locate(7, 0)
    print(f"[ＬＩＦＥ：{life:>2}]")
    locate(26, 0)
    print(f"[ＳＣＯＲＥ：{score:>5}]")
    locate(50, 0)
    print(f"[ＨＩＳＣＯＲＥ：{hiscore:>5}]")


def opening():
    global hiscore, score
    hiscore = score = 0
    cls(True)
    print_title(0, 0, char=BODY, wchar=True,
                title=("11        112 111     1111111   111  111",
                       " 1   111  1  11   21  1     11 11 1 11 1",
                       " 11  1 1  1 11     11 1      1 1  1 1  1",
                       "  1  1 1  1 1       1 1      1 1  1 1  1",
                       "  1  1 1  1 1       1 1  11111 1  111  1",
                       "  11 1 1 11 11     11 1  1     1       1",
                       "   1 1 1 1   11   11  1  11    1       1",
                       "   111 111    11111   1   1112 1      11",
                       "                                      1 ",
                       "                                      1 ",
                       "                                      1 ",
                       "                                      2 "))
    color(C_TEXT)
    print_message(0, 9,
                  ("　Ｃｏｎｔｒｏｌ　ｔｈｅ　ｗｏｒｍ　ｓｏ　"
                   "ｔｈａｔ　ｉｔ　ｄｏｅｓ　ｎｏｔ",
                   "ｈｉｔ　ｗａｌｌｓ　ａｎｄ　ｉｔｓｅｌｆ．"
                   "　Ｔａｋｅ　ａｌｌ　ｆｒｕｉｔｓ",
                   "　　ｔｏ　ｃｌｅａｒ　ｔｈｅ　ｓｔａｇｅ．"
                   "　　（Ｃ）２０２３　ｎｏｚｗａｓ"),
                  spacing=1)
    print_frame(0, 15, 20, 9, K7+K9+K1+K3+KH+KV, True)
    print_frame(20 * 2, 15, 20, 9, K7+K9+K1+K3+KH+KV, True)
    print_at(2 * 2, 15, " ＣＨＡＲＡＣＴＥＲＳ ")
    print_at(8 * 2, 17, " ．．． ＷＯＲＭ")
    print_at(8 * 2, 19, " ．．． ＷＡＬＬＳ")
    print_at(8 * 2, 21, " ．．． ＦＲＵＩＴＳ")
    print_at(22 * 2, 15, " ＯＰＥＲＡＴＩＯＮＳ ")
    print_frame(33 * 2, 17, 3, 3, K7+K9+K1+K3+KH+KV, True)
    print_at(34 * 2, 18, A8)  # up
    print_frame(30 * 2, 20, 3, 3, K7+K9+K1+K3+KH+KV, True)
    print_at(31 * 2, 21, A4)  # left
    print_frame(33 * 2, 20, 3, 3, K7+K9+K1+K3+KH+KV, True)
    print_at(34 * 2, 21, A2)  # down
    print_frame(36 * 2, 20, 3, 3, K7+K9+K1+K3+KH+KV, True)
    print_at(37 * 2, 21, A6)  # right
    print_at(22 * 2, 17, "Ｍｏｖｉｎｇ")
    print_at(22 * 2, 18, "　ｄｉｒｅｃｔｉｏｎ")
    print_at(3 * 2, 24, "Ｐｕｓｈ ［Ｓ］ ｋｅｙ　ｔｏ　Ｓｔａｒｔ　"
                        "ｏｒ ［Ｑ］ ｔｏ　Ｑｕｉｔ")
    print_at(2 * 2, 17, BODY * 4, C_BLOCK)
    print_at(6 * 2, 17, WORM, C_WORM)
    print_at(2 * 2, 19, WALL * 2, C_WALL)
    t_fill(5 * 16, 19 * 16, 7 * 16 - 1, 20 * 16 - 1, 0b0100)
    print_at(5 * 2, 19, BLOCK * 2, C_BLOCK)
    color(C_WALL)
    locate(2 * 2, 21)
    t_fill(4 * 16, 21 * 16, 5 * 16 - 1, 22 * 16 - 1, 0b0100)
    t_fill(6 * 16, 21 * 16, 7 * 16 - 1, 22 * 16 - 1, 0b1100)
    for s in FRUITS:
        print(s + SP, end="")
        

def game_start():
    global life, score, hiscore
    hiscore = score if score > hiscore else hiscore
    life, score = 5, 0


def new_stage():
    global tbuf
    cls(True)    
    tbuf = [["\x00"] * 40 for y in range(25)]
    tpalet2(3, (rgb(31, 0, 0), rgb(31, 31, 0), rgb(31, 0, 31))[stage - 1])
    t_fill(0, 0, 40 * 16 - 1, 15, 0b0100)
    color(C_BLOCK)
    print("=" * 80)
    print_score()
    color(C_WALL)
    locate(0, 1)
    print(WALL * 40); tbuf[1] = [WALL] * 40
    for i in range(2, 24):
        locate(0, i)
        print(WALL * 2 + SP * 36 + WALL * 2, end="")
        tbuf[i] = [WALL] * 2 + [SP] * 36 + [WALL] *2
    locate(0, 24)
    print(WALL * 40, end=""); tbuf[24] = [WALL] * 40
    if stage == 2:
        locate(10 * 2, 8)
        print(WALL * 20); tbuf[8][10:30] = [WALL] * 20
        locate(10 * 2, 17)
        print(WALL * 20); tbuf[17][10:30] = [WALL] * 20
    elif stage == 3:
        locate(6 * 2, 8)
        print(WALL * 20); tbuf[8][6:26] = [WALL] * 20
        locate(14 * 2, 17)
        print(WALL * 20); tbuf[17][14:34] = [WALL] * 20
        for i in range(3):
            locate(6 * 2, 7 - i)
            print(WALL); tbuf[7 - i][6] = WALL
            locate(33 * 2, 18 + i)
            print(WALL); tbuf[18 + i][33] = WALL
    locate(20 * 2, 13)
    print(WORM); tbuf[13][20] = WORM
    color(C_FRUITS)
    for i in range(3):
        while True:
            x, y = randrange(36) + 2, randrange(22) + 2
            if tbuf[y][x] == SP:
                locate(x * 2, y)
                print(FRUITS[stage - 1]); tbuf[y][x] = FRUITS[stage - 1]
                break
    

def game_over():
    print_score()
    tpalet2(3, rgb(31, 31, 31))
    print_message(6 * 2, 8, [K7+SP+K7+KH+K9+K7+KH+K9+K8+K8+K8+K8+KH+K9+
                             K7+KH+K9+K8+SP+K8+K8+KH+K9+K8+KH+K9+SP+K9,
                             KV+SP+KV+SP+K9+K4+KH+K6+KV+KV+KV+K4+K6+SP+
                             KV+SP+KV+KV+K7+K3+K4+K6+SP+K4+K8+K3+SP+KV,
                             K1+SP+K1+KH+K3+K2+SP+K2+K2+SP+K2+K2+KH+K3+
                             K1+KH+K3+K1+K3+SP+K2+KH+K3+K2+K1+K3+SP+K3], 
                             3)
    print_message(10 * 2, 15,
                  ("Ｐｕｓｈ ［Ｓ］ ｋｅｙ　ｔｏ　Ｓｔａｒｔ",
                   "　　　　 ［Ｑ］ ｋｅｙ　ｔｏ　Ｑｕｉｔ",
                   "　　　　 ［Ｃ］ ｋｅｙ　ｔｏ　Ｃｏｎｔｉｎｕｅ"))
    a_play(PCM1, 0, 0b11, 512)


def ending():
    print_score()
    tpalet2(3, rgb(31, 31, 31))
    print_message(4 * 2, 2, [K7+SP+K7+KH+K9+K7+KH+K9+K8+K8+K8+K8+KH+K9+SP+K7+
                             KH+K9+K8+SP+SP+K8+KH+K9+K7+KH+K9+K8+KH+K9+SP+K9,
                             KV+SP+KV+SP+K9+K4+KH+K6+KV+KV+KV+K4+K6+SP+SP+KV+
                             SP+SP+KV+SP+SP+K4+K6+SP+K4+KH+K6+K4+K8+K3+SP+KV,
                             K1+SP+K1+KH+K3+K2+SP+K2+K2+SP+K2+K2+KH+K3+SP+K1+
                             KH+K3+K2+KH+K3+K2+KH+K3+K2+SP+K2+K2+K1+K3+SP+K3],
                             3)
    t_fill(0, 5 * 16, 40 * 16 - 1, 21 * 16 -1, 0b1000)
    t_fill(0, 5 * 16, 40 * 16 - 1, 11 * 16 -1, 0b0100, style= 0x0000)
    t_fill(2 * 16, 11 * 16, 38 * 16 - 1, 21 * 16 -1, 0b0100)
    for i, c in enumerate(((0, 0, 0), (6, 6, 6), (31, 0, 0), (4, 4, 4),
                          (0, 0, 0), (6, 6, 6), (8, 8, 8), (0, 31, 0)),
                          start=8):
        tpalet2(i, rgb(c[0], c[1], c[2]))
    print_title(0, 5, char=FILL, wchar= True,
                title=["   ...3333...  ..........  ...3333...   ",
                       " ...33333333....33....33....33333333... ",
                       "..333331111111....3..3....111111133333..",
                       "3333111221111111..3..3..1111111221113333",
                       "33311122221133111..22..11133112222111333",
                       ".31111121221133111.22.11133112212111113.",
                       "..111111111111111113311111111111111111..",
                       " ...11113311111211133111211111331111... ",
                       "   ...1113311122111331112211133111...   ",
                       "     ...111111221113311122111111...     ",
                       "      ...1112221111331111222111...      ",
                       "     ..11122211111133111111222111..     ",
                       "     .111111111111.33.111111111111.     ",
                       "   ...11113311111..33..11111331111...   ",
                       "  ..333311111......33......111113333..  ",
                       "  .3333.......    ....    .......3333.  ",
                       "   ....                          ....   "])
    for i, c in enumerate(((0, 0, 0), (0, 0, 31), (31, 0, 0), (31, 31, 0),
                          (0, 0, 0), (0, 0, 31), (31, 0, 31), (0, 31, 0)),
                          start=8):
        tpalet2(i, rgb(c[0], c[1], c[2]))
    print_message(10 * 2, 21,
                  ("Ｐｕｓｈ ［Ｓ］ ｋｅｙ　ｔｏ　Ｓｔａｒｔ",
                   "　　　　 ［Ｑ］ ｋｅｙ　ｔｏ　Ｑｕｉｔ"), C_TEXT)
    a_play(PCM1, 3, 0b11, 384)


def game_play():
    global stage, score, life, tbuf
    x, y = 20, 13
    dx, dy = -1, 0
    fruit = 3

    new_stage()

    waiting = 2
    keyflush()
    while waiting:
        color(waiting)
        locate(x * 2, y)
        print(WORM)
        waiting = 2 // waiting
        k = inkey0()
        if k == K_LEFT or k == K_s:
            dx, dy, waiting = -1, 0, 0
        elif k == K_RIGHT:
            dx, dy, waiting = 1, 0, 0
        elif k == K_UP:
            dx, dy, waiting = 0, -1, 0
        elif k == K_DOWN:
            dx, dy, waiting = 0, 1, 0
        elif k == K_q or k == K_ESCAPE:
            life = 0
            return MISTAKE
        for i in range(GAME_SPEED):
            x68k.vsync()

    while True:
        k = inkey(0)
        if k == K_LEFT and dx != 1:
            dx, dy = -1, 0
        elif k == K_RIGHT and dx != -1:
            dx, dy = 1, 0
        elif k == K_UP and dy != 1:
            dx, dy = 0, -1
        elif k == K_DOWN and dy != -1:
            dx, dy = 0, 1
        elif k == K_s:
            keyflush()
            inkey()
        color(1)
        locate(x * 2, y)
        print(BODY); tbuf[y][x] = BODY
        x += dx
        y += dy
        p = tbuf[y][x]
        color(2)
        locate(x * 2, y)
        print(WORM); tbuf[y][x] = WORM
        if p in FRUITS:
            a_play(PCM1, 2, 0b11, 256)
            fruit -= 1
            score += 100
            if fruit == 0:
                stage += 1
                return GAME_CLEAR if stage > 3 else STAGE_CLEAR
        elif p in (WALL, BLOCK, BODY):
            a_play(PCM1, 1, 0b11, 192)
            life -= 1
            return MISTAKE
        score += 1
        if score % 5 == 0:
            wx, wy = randrange(36) + 2, randrange(22) + 2
            if tbuf[wy][wx] == SP:
                color(C_BLOCK)
                locate(wx * 2, wy)
                t_fill(wx * 16, wy * 16, wx * 16 + 15, wy * 16 + 15, 0b0100)
                print(BLOCK); tbuf[wy][wx] = BLOCK
        color(C_TEXT)
        locate(39, 0)
        print(f"{score:>5}")
        for i in range(GAME_SPEED):
            x68k.vsync()


def main():
    global stage
    global C_WORM, C_BODY, C_WALL, C_BLOCK, C_FRUITS, C_TEXT
    global K_UP, K_LEFT, K_RIGHT, K_DOWN, K_ESCAPE, K_s, K_q, K_c
    global WORM, BODY, WALL, BLOCK, FILL, FRUITS, FRUIT1, FRUIT2, FRUIT3
    global A6, A4, A8, A2, KH, KV, K7, K8, K9, K4, K5, K6, K1, K2, K3, SP
    global PCM1

    width(96)
    console(0, 32, 0)
    cursor_off()
    pat = ("07e01ff83ffc7ffe7ffef3cff3cff3cfffffffffffff6ff673ce3c3c1ff807e0",
           "07e01ff83ffc7ffe7ffeffffffffffffffffffffffff7ffe7ffe3ffc1ff807e0",
           "fffcfffcfffcfffcfffcfffc00000000fcfffcfffcfffcfffcfffcff00000000", 
           "7ffcbffadff6eaaef55eeaaef55eeaaef55eeaaef55eeaaedff6bffa7ffc0000",
           "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
           "00e001c001001f787bfcfc7efffffffffffffffffff7fff77fee7ffe3ffc0ff0",
           "007e00080018003c007e00f601f703ef07cf0f9f3f1efe3e7c7c01f80ff007e0",
           "0006001e007000a00120022004203c107e3cff7efeffdeffeedf7eef3c7e003c")
    for code, p in enumerate(pat, start=0xed40):
        deffont(code, unhexlify(p))
    (WORM, BODY, WALL, BLOCK, FILL, FRUIT1, FRUIT2, 
     FRUIT3) = map(lambda i: chr(i), range(0xed40, 0xed40 + len(pat)))
    FRUITS = (FRUIT1, FRUIT2, FRUIT3)
    (A6, A4, A8, A2, KH, KV, K7, K8, K9, K4, K5, K6, 
     K1, K2, K3, SP) = ("→", "←", "↑", "↓", "━", "┃", "┏", "┳", "┓", 
                        "┣", "╋", "┫", "┗", "┻", "┛", "　")
    pal = ((0, 0, 0), (0, 31, 0), (31, 0, 0), (31, 31, 31),
           (0, 0, 0), (0, 31, 31), (31,31, 0), (31, 31, 31),
           (0, 0, 0), (0, 0, 31), (31, 0, 0), (31, 31, 0),
           (0, 0, 0), (0, 0, 31), (31, 0, 31), (0, 31, 0))
    for i, c in enumerate(pal):
        tpalet2(i, rgb(c[0], c[1], c[2]))
    C_WORM, C_BODY, C_WALL, C_BLOCK, C_FRUITS, C_TEXT = 2, 1, 2, 1, 3, 7
    K_ESCAPE, K_s, K_q, K_c = 27, ord("s"), ord("q"), ord("c")
    K_UP, K_LEFT, K_RIGHT, K_DOWN = 0x10, 0x02, 0x06, 0x0e
    for i, code in enumerate((K_UP, K_LEFT, K_RIGHT, K_DOWN), start=25):
        key(i, chr(code).encode())

    PCM1 = unhexlify("7077fd0f" + "3481bd19" * 127)

    opening()

    stage = 1
    while True:
        k = inkey()
        if k == K_s:
            stage = 1
            k = K_c
        if k == K_c:
            game_start()
            while life > 0:
                g = game_play()
                if g == GAME_CLEAR:
                    ending()
                    stage = 1
                    break
                elif g == STAGE_CLEAR:
                    pass
                elif g == MISTAKE:
                    pass
            if life == 0:
                game_over()
        elif k == K_q or k == K_ESCAPE:
            break

    cls(True)
    end()
    

main()
