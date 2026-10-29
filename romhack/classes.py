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
    def __init__(self, start: int, picks: int):
        self.title = None
        self.start = start
        self.picks = picks
        self.rooms = [None for i in range(NUM_ROOMS)]

    def set_title(self, title: Room):
        self.title = title

    def add_room(self, room: Room, location: int):
        if len(room.sprites) > 14:
            print("Warning, too many sprites in room " + hex(location) + ". 15th sprite is buggy, and any more won't spawn. Truncating to 14 sprites")
            room.sprites = room.sprites[:14]
        self.rooms[16*(location >> 4) + (location & 0x0F)] = room

    # combine another map with yourself. Throw an assert if the other map has a non-empty room in the same place as you
    def merge(self, other: Map):
        for i in range(NUM_ROOMS):
            if self.rooms[i] == None:
                self.rooms[i] = other.rooms[i]
            else:
                assert other.rooms[i] == None, "Map merge conflict on room " + hex(i) + "\n" + print_data(other.rooms[i].uncompressed)

    # shift the whole map. useful to line up two maps before merging.
    # For example, if you wanted to shift everything so that room 0xPP
    # is now room 0xQQ, call your_map.shift(0xQQ - 0xPP)
    def shift(self, shift: int):
        self.rooms = [self.rooms[(i - shift) % NUM_ROOMS] for i in range(NUM_ROOMS)]


def print_data(data):
    out = ""
    for i, datum in enumerate(data):
        out += format(data[i], "02X")
        if i % 16 == 15:
            out += '\n'
        else:
            out += " "
    return out
