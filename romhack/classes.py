from dataclasses import dataclass

NUM_ROOMS = 256

@dataclass
class Sprite():
    id: int
    position: int

@dataclass
class Room():
    zone: int               # zone number [0, 4] inclusive
    uncompressed: list[int] # list of 240 tiles
    sprites: list[Sprite]

@dataclass
class Map():
    name: str               # used to name new rom file
    title: int              # hexcode location of title screen
    start: int              # hexcode location of the screen you start falling from
    picks: int              # bitfield of picks you start the game with        
    rooms: list[Room]

class Map():
    def __init__(self, title: int, start: int, picks: int):
        self.title = title
        self.start = start
        self.picks = picks
        self.rooms = [None for i in range(NUM_ROOMS)]

    def add_room(self, room: Room, location: int):
        self.rooms[16*(location >> 4) + (location & 0x0F)] = room