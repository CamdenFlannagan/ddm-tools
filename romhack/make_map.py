from compress_room import compress
from classes import Sprite, Room, Map

# --------------------------------------------- #
# Constants
# --------------------------------------------- #
CPU_MEM_OFFSET  = -0x7FF0 # address in cpu memory + CPU_MEM_OFFSET = where in rom file is data
ROOM_ADDR_LOWER =  0xf213
ROOM_ADDR_UPPER =  0xf313
ROOM_ZONE       =  0xf413

PRG_ROM_OFFSET  =  0x0010
ROOM_DATA_START =  0x9426
EMPTY_ROOM      =  ROOM_DATA_START

NUM_ROOMS = 256

# tiles that you cannot perform a room transition through
no_transition = set([
    *[i for i in range(0x01, 0x14)], # dirts
    *[i for i in range(0x18, 0x27)], # metals
    *[i for i in range(0x7d, 0x82)], # dirts
    0xAF,                            # title grass
    *[i for i in range(0xb8, 0xd7)], # dirts
])

'''
when drawing the in-game map:
up is bit 0
down is bit 1
left is bit 2
right is bit 3

+

zone 00 is C1
zone 01

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

def hack_da_rom(map: Map, original_rom: str, new_rom: str):
    bytes_used = 0

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
    rom_hacked.seek(0xC7C5 + CPU_MEM_OFFSET) # which room contains the title screen. 0xC7C5 in CPU Memory
    rom_hacked.write(map.title.to_bytes(1))

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

    # ----------------------------------------- #
    # Close new rom file
    # ----------------------------------------- #
    rom_hacked.close()

    return bytes_used
