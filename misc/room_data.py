'''
Needs rom at placed at and titled ../roms/ddm.nes
Run program with room number (in hex) as argument
'''

import sys

room = int(sys.argv[1], 16)

with open("../roms/ddm.nes", "rb") as f:
    f.seek(0xf213 + room - 0x7ff0)
    room_addr_2 = f.read(1)
    f.seek(0xf313 + room - 0x7ff0)
    room_addr_1 = f.read(1)

    room_addr = int.from_bytes(room_addr_2) + (int.from_bytes(room_addr_1) << 8)

    f.seek(room_addr + 0x0010)

    room_data = f.read(0x100)

    room_data = [room_data[i] for i in range(len(room_data))]

    out = ""

    for i in range(16):
        for j in range(16):
            out += format(room_data[16*i + j], "02X") + " "
        out += "\n"

    print("PRGM ROM " + hex(room_addr))
    print(out)
    