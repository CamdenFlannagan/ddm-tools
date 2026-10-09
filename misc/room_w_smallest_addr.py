
with open("../roms/ddm.nes", "rb") as f:
    least_addr = 0xFFFF
    least_room = 0
    for room in range(256):
        f.seek(0xf213 + room - 0x7ff0)
        room_addr_2 = f.read(1)
        f.seek(0xf313 + room - 0x7ff0)
        room_addr_1 = f.read(1)

        room_addr = int.from_bytes(room_addr_2) + (int.from_bytes(room_addr_1) << 8)

        if room_addr < least_addr:
            least_addr = room_addr
            least_room = room
    print(hex(least_room) + ": " + hex(least_addr))