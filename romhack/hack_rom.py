from compress_room import compress
from classes import Sprite, Room, Map
from in_game_map import in_game_map

# --------------------------------------------- #
# CPU Memory Constants
# --------------------------------------------- #
CPU_MEM_OFFSET        = -0x7FF0 # address in cpu memory + CPU_MEM_OFFSET = where in rom file is data

CHEST_ROOM_LOCATION   =  0xcb38

# MAP_CHEST_POSITION is 0xdfbe
MAP_CHEST_TILE        =  0xdfa5
# MAP_CHEST_ORIENTATION_AND_COLOR is 0xdfcb

# MAP_BOMB_POSITION is 0xdfa1
MAP_BOMB_TILE         =  0xdfc2
# MAP_BOMB_ORIENTATION_AND_COLOR is 0xdfa9

# MAP_DOTS_POSITIONS starts 0xf20a, 9 bytes for 9 positions
MAP_DOTS_TILE         =  0xdfe0
# MAP_DOTS_ORIENTATION_AND_COLOR is 0xdfef

ROOM_ADDR_LOWER       =  0xf213
ROOM_ADDR_UPPER       =  0xf313
ROOM_ZONE             =  0xf413

MAP_TILE_DATA         =  0xf513
MAP_TILE_DATA_LEN     =  0x100

MAP_PALLETE_DATA      =  0xf613
MAP_PALLETE_DATA_LEN  =  0x14

# --------------------------------------------- #
# PRG ROM Constants
# --------------------------------------------- #
PRG_ROM_OFFSET  =  0x0010

ROOM_DATA_START =  0x9426
EMPTY_ROOM      =  ROOM_DATA_START

# --------------------------------------------- #
# Other Constants
# --------------------------------------------- #
NUM_ROOMS = 256

def hack_da_rom(map: Map, original_rom: str, new_rom: str, make_in_game_map: bool = False):
    bytes_used = 0 # keep track of how many bytes we've used for level data, just for fun

    # ----------------------------------------- #
    # Create new rom file
    # ----------------------------------------- #
    rom_data = b'0'
    with open(original_rom, "rb") as rom_old:
        rom_data = rom_old.read()
    rom_hacked = open(new_rom, "wb+")
    rom_hacked.write(rom_data)

    # ---------------------------------------- #
    # Set the title screen
    # ----------------------------------------- #
    some_empty_room = 0x00
    for i in range(NUM_ROOMS):
        if map.rooms[i] == None:
            some_empty_room = i
            break
    map.rooms[some_empty_room] = map.title
    rom_hacked.seek(0xC7C5 + CPU_MEM_OFFSET) # which room contains the title screen. 0xC7C5 in CPU Memory
    rom_hacked.write(some_empty_room.to_bytes(1))

    # ----------------------------------------- #
    # Set the starting room
    # ----------------------------------------- #
    rom_hacked.seek(0xC9F8 + CPU_MEM_OFFSET) # which room mr. diggy diggy starts falling from. 0xC9F8 in CPU Memory
    rom_hacked.write(map.start.to_bytes(1))

    # ----------------------------------------- #
    # Set the starting room
    # ----------------------------------------- #
    rom_hacked.seek(0x9706 + CPU_MEM_OFFSET) # what picks mr. diggy diggy starts the main quest with. 0x9706 in CPU Memory
    rom_hacked.write(map.picks.to_bytes(1))

    # ----------------------------------------- #
    # Fill the rom with the new room data
    # ----------------------------------------- #
    room_data_cursor = ROOM_DATA_START
    rom_hacked.seek(room_data_cursor + PRG_ROM_OFFSET)
    
    # --------------------------------- #
    # Make empty room
    # --------------------------------- #
    rom_hacked.write(b'\xff\x00\xf1\x7f\x00\x00')
    room_data_cursor += 6

    # --------------------------------- #
    # Fill with custom rooms
    # --------------------------------- #
    for i in range(NUM_ROOMS):
        if map.rooms[i] == None: # empty room
            rom_hacked.seek(ROOM_ZONE + CPU_MEM_OFFSET + i)
            rom_hacked.write(0x00.to_bytes(1))
            rom_hacked.seek(ROOM_ADDR_LOWER + CPU_MEM_OFFSET + i)
            rom_hacked.write((EMPTY_ROOM & 0xFF).to_bytes(1))
            rom_hacked.seek(ROOM_ADDR_UPPER + CPU_MEM_OFFSET + i)
            rom_hacked.write(((EMPTY_ROOM >> 8) & 0xFF).to_bytes(1))
        else:
            rom_hacked.seek(ROOM_ZONE + CPU_MEM_OFFSET + i)
            rom_hacked.write(map.rooms[i].zone.to_bytes(1))
            rom_hacked.seek(ROOM_ADDR_LOWER + CPU_MEM_OFFSET + i)
            rom_hacked.write((room_data_cursor & 0xFF).to_bytes(1))
            rom_hacked.seek(ROOM_ADDR_UPPER + CPU_MEM_OFFSET + i)
            rom_hacked.write(((room_data_cursor >> 8) & 0xFF).to_bytes(1))

            rom_hacked.seek(room_data_cursor + PRG_ROM_OFFSET)
            data = compress(map.rooms[i])
            bytes_used += len(data)
            rom_hacked.write(data)
            room_data_cursor += len(data)

    # --------------------------------- #
    # Set the chest room to be some
    # empty room, to avoid the fadeout
    # transition bothering the gameplay
    # --------------------------------- #
    rom_hacked.seek(CHEST_ROOM_LOCATION + CPU_MEM_OFFSET)
    rom_hacked.write(some_empty_room.to_bytes(1))

    # ----------------------------------------- #
    # Make in-game map match our custom map
    # ----------------------------------------- #
    if make_in_game_map:
        # make all of the usual map sprites invisible
        rom_hacked.seek(MAP_BOMB_TILE + CPU_MEM_OFFSET)
        rom_hacked.write(0x00.to_bytes(1))
        rom_hacked.seek(MAP_CHEST_TILE + CPU_MEM_OFFSET)
        rom_hacked.write(0x00.to_bytes(1))
        rom_hacked.seek(MAP_DOTS_TILE + CPU_MEM_OFFSET)
        rom_hacked.write(0x00.to_bytes(1))

        # draw our new map!
        map_tile_data, map_pallete_data = in_game_map(map)
        rom_hacked.seek(MAP_TILE_DATA + CPU_MEM_OFFSET)
        rom_hacked.write(bytes(map_tile_data))
        rom_hacked.seek(MAP_PALLETE_DATA + CPU_MEM_OFFSET)
        rom_hacked.write(bytes(map_pallete_data))

    # ----------------------------------------- #
    # Close new rom file
    # ----------------------------------------- #
    rom_hacked.close()

    return bytes_used
