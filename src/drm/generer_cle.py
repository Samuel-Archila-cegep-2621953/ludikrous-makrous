import os

cle = os.urandom(32)

def _hex(b: int) -> str:
    _s = hex(b)[2:]
    if len(_s) == 1: return '0' + _s
    return _s

for b in cle:
    print(f"(unsigned char)0x{_hex(b)},")