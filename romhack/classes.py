from dataclasses import dataclass

NUM_ROOMS = 256

@dataclass
class Sprite():
    id: int
    position: int

class Room():
    def __init__(self, zone: int, uncompressed: int, sprites: list[Sprite]):
        self.zone = zone
        self.uncompressed = uncompressed
        self.sprites = sprites

class Map():
    def __init__(self, title: int, start: int, picks: int):
        self.title = title
        self.start = start
        self.picks = picks
        self.rooms = [None for i in range(NUM_ROOMS)]

    def add_room(self, room: Room, location: int):
        if len(room.sprites) > 14:
            print("Warning, too many sprites in room " + hex(location) + ". 15th sprite is buggy, and any more won't spawn. Truncating to 14 sprites")
            room.sprites = room.sprites[:14]
        self.rooms[16*(location >> 4) + (location & 0x0F)] = room

def print_data(data):
    out = ""
    for i, datum in enumerate(data):
        out += format(data[i], "02X")
        if i % 16 == 15:
            out += '\n'
        else:
            out += " "
    print(out)
