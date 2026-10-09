room_addrs = [(0, 0) for i in range(256)]
with open("../roms/ddm.nes", "rb") as f:
    for room in range(256):
        f.seek(0xf213 + room - 0x7ff0)
        room_addr_2 = f.read(1)
        f.seek(0xf313 + room - 0x7ff0)
        room_addr_1 = f.read(1)

        room_addr = int.from_bytes(room_addr_2) + (int.from_bytes(room_addr_1) << 8)

        room_addrs[room] = (room, room_addr)

room_addrs = sorted(room_addrs, key=lambda x: x[1])
room_addrs = [(hex(room[0]), hex(room[1])) for room in room_addrs]
print(room_addrs)
