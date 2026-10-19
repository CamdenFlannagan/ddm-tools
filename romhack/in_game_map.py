from dataclasses import dataclass
from classes import Sprite, Room, Map

MAP_TILE_DATA_LEN    = 0x100
MAP_PALLETE_DATA_LEN = 0x14

EMPTY_ROOM = -1

'''
when drawing the in-game map:
up is bit 0
down is bit 1
left is bit 2
right is bit 3

+

zone 00 is Green
zone 01 is Yellow
zone 02 is Purple
zone 03 is Red

+

Pallet 0
Green = Green
Yellow = Yellow
Purple = Purple

Pallete 1
Green = Yellow
Yellow = Purple
Purple = Red

Pallete 2
Green = Purple
Yellow = Red
Purple = Green

Pallete 3
Green = Red
Yellow = Green
Purple = Yellow

'''
pallete_to_color_index = [  
    [0, 1, 2, None],
    [None, 0, 1, 2],
    [2, None, 0, 1], # example, in pallete 2, red zones (zone 3) should have a color index of 1, pal_2_clr_idx[2][3] = 1
    [1, 2, None, 0],
]


# palletes get set in groups of 4 tiles (the little 8x8 tiles, not 16x16 tiles).
# if you split up the map into a bunch of 16x16 squares, you would get all of the quads (groups of 4 tiles) on the map.
@dataclass
class Quad():
    y: int
    x: int


# tiles that you cannot perform a room transition through
no_transition = set([
    *[i for i in range(0x01, 0x14)], # dirts
    *[i for i in range(0x18, 0x27)], # metals
    *[i for i in range(0x7d, 0x82)], # dirts
    0xAF,                            # title grass
    *[i for i in range(0xb8, 0xd7)], # dirts
])


''' works '''
def room_edges(room: Room):
    data = room.uncompressed
    result = 0

    # upper edge
    for i in range(16):
        if data[i] not in no_transition:
            result += 1
            break

    # lower edge
    for i in range(16):
        if data[16*14 + i] not in no_transition:
            result += 2
            break

    # left edge
    for i in range(15):
        if data[16*i] not in no_transition:
            result += 4
            break

    # right edge
    for i in range(15):
        if data[16*i + 15] not in no_transition:
            result += 8
            break

    assert result > 0, "this room has NO transitionable edges: " + data

    return result - 1 # minus one because there is no tile for a room with no edges


'''
n, map pallete data index
return, y and x coordinates of all for quads in the pallete data square
'''
def pallete_data_idx_to_quads(n: int) -> list[Quad]:
    return [
        Quad(2*(n // 4), 2*(n % 4)),
        Quad(2*(n // 4), 2*(n % 4) + 1),
        Quad(2*(n // 4) + 1, 2*(n % 4)),
        Quad(2*(n // 4) + 1, 2*(n % 4) + 1),
    ]


def yx_to_hex(yx: tuple[int, int]) -> int:
    assert yx[0] < 16, yx
    assert yx[1] < 16, yx
    return (yx[0] << 4) + yx[1]


def quad_to_pallete_data_idx(quad: Quad):
    return (4*(quad.y//2)) + (quad.x//2)


def quad_to_rooms(quad: Quad) -> list[int]:
    return [
        yx_to_hex((2*(quad.y - 1), 2*quad.x)),
        yx_to_hex((2*(quad.y - 1), 2*quad.x + 1)),
        yx_to_hex((2*(quad.y - 1) + 1, 2*quad.x)),
        yx_to_hex((2*(quad.y - 1) + 1, 2*quad.x + 1)),
    ]


def zones_to_pallete_and_color_idxs(zones: list[int]) -> tuple[int, list[int]]:
    assert len(zones) == 4, "must provide exactly 4 zones to this function"
    assert len(set(zones)) < 4, "you may only have 3 or fewer unique zones per quad"
    for zone in zones:
        assert zone < 4, "zones must be less than or equal to 3"

    # Make empty rooms have the zone of another room in this quad
    # if all are empty, give them all zone 0
    for i in range(len(zones)):
        if zones[i] == EMPTY_ROOM:
            non_empties = [zone for zone in zones if zone != EMPTY_ROOM]
            zones[i] = 0 if len(non_empties) == 0 else non_empties[0]

    assert len(zones) == 4, "ok if this ever fails, that's my fault and the code is borked"

    if 0 not in zones:
        return 1, [pallete_to_color_index[1][zone] for zone in zones]
    elif 1 not in zones:
        return 2, [pallete_to_color_index[2][zone] for zone in zones]
    elif 2 not in zones:
        return 3, [pallete_to_color_index[3][zone] for zone in zones]
    elif 3 not in zones:
        return 0, [pallete_to_color_index[0][zone] for zone in zones]
                
    # i don't think reaching this code is possible. the asserts would stop that from happening
    return None, None


def in_game_map(map: Map):
    map_tile_data = [0x00 for i in range(MAP_TILE_DATA_LEN)]
    map_pallete_data = [0x00 for i in range(MAP_PALLETE_DATA_LEN)]

    for pallete_data_idx in range(MAP_PALLETE_DATA_LEN):
        
        quads = pallete_data_idx_to_quads(pallete_data_idx)
        for quad_idx, quad in enumerate(quads):
            if quad.y <= 0 or quad.y >= 9: # edgy quads with OOB rooms (room < 0 or room >= 256)
                continue
        
            rooms = quad_to_rooms(quad)
            zones = [EMPTY_ROOM if map.rooms[room] == None else map.rooms[room].zone for room in rooms]
            pallete, color_idxs = zones_to_pallete_and_color_idxs(zones)

            # set pallete data using the pallete value
            map_pallete_data[pallete_data_idx] |= pallete << (2*quad_idx)

            for room_idx, room in enumerate(rooms):
                assert room < 0x100, "Room OOB. room: " + hex(room) + ", quad:" + quad + ", pal idx: " + pallete_data_idx

                if map.rooms[room] == None:
                    map_tile_data[room] = 0x00
                else:
                    map_tile_data[room] = 0xC1 + room_edges(map.rooms[room]) + (0x10*color_idxs[room_idx])

    return map_tile_data, map_pallete_data

                