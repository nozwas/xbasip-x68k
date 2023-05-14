# -*- coding: shift_jis -*-
# xbasip sample programs
# nozwas <https://github.com/nozwas>

r"""sample04.py
    audioモジュール、musicモジュールの使用例
"""

from xbasip.console import *
from xbasip.audio import *
from xbasip.music import *
from binascii import unhexlify

def wait_while_playing(func):
    keyflush()
    while func() != 0:
        if inkey0() == 27: # ESC key
            if func == m_stat:
                m_stop()
            end("途中で終了します。")

keyflush()
print("ADPCMデータを再生します。何かキーを押してください。")
inkey()
pcm = unhexlify("7077fd0f" + "3481bd19" * 127)
for freq in range(5):
    a_play(pcm, freq, 0b11, 512)
    wait_while_playing(a_stat)

print("FM音源データを再生します。何かキーを押してください。")
inkey()

try:
    m_init()
except:
    end("musicモジュールを使用するには、opmdrv3もしくは"
        "zmusic2をシステムに組み込んでおく必要があります。")

VO1 = (58, 15, 0,  0,  0,  0, 0, 0, 0, 3, 0,
       14, 14, 0,  3,  1, 27, 2, 1, 3, 0, 0,
       14, 14, 0,  3, 15, 37, 2, 7, 2, 0, 0,
       13, 14, 0,  3,  1, 37, 2, 1, 4, 0, 0,
       19,  3, 0, 10,  0,  0, 1, 1, 6, 0, 1)

VO234 = ("3a0f000000000000000300"
         "100c0008001c00010000000e0e000a0f280002000200"
         "140e000a07310001000000100e000801000001000001",
         "3c0f0000c8000000000300"
         "120c010a02200101000000120a010a03000001010001"
         "0f0a010a051301010200001402010a03070001060001",
         "320f000000000000000300"
         "1f00000f001901030000001f00000f0023030c040001"
         "1f000002002401010000001f0604050f000201040001")

m_vset(1, bytes(VO1)) # 整数配列から

for v, dat in enumerate(VO234, start=2):
    m_vset(v, unhexlify(dat)) # 文字列から

for i in range(6):
    m_alloc(i + 1, 2000)
    m_assign(i + 1, i + 1)

m_trk(1, "q7@1v9o4t66")
m_trk(2, "q7@2v10o4")
m_trk(3, "q7@3v10o3")
m_trk(4, "q8@4v8o5")
m_trk(5, "q8@4v8o5")
m_trk(6, "q8@4v8o4")

mml = ("l16b-4&b-b-agf8g8de-f8:<r8f8&fe-dc>b-8<d8>ab-<c8"
       ">f<fd>b-<e-8g8&ge-c>a&a8<f8:d4e4f8>b-4a8",
       "l16r1:>b-fb-<dc8e-8&e-8de{fefefefe}8&ed32e32"
       "f4g8b-8e-8g8<c8c8&:c>fb-<d>g8b-8a8de-fge-f",
       "l8b-<dc>b-agfe-:d4f4g4<c4"
       "d4&l16dd>b-g<c8e-8&e-c>af:b-4&b-b-agf8g8de-f8")       
for t, m in enumerate(mml):
    m_trk(t + 1, m)
    m_trk(t + 4, m)

m_play()
wait_while_playing(m_stat)
