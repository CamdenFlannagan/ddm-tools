import sys
import argparse
import numpy as np

ROOM_HEIGHT = 240
ROOM_WIDTH = 256
NUM_ROOMS = 256

def hex_int(x):
    return int(x, 16)

parser = argparse.ArgumentParser(description="Diggy Diggy Mole Randomizer")
parser.add_argument("--seed", type=int, default=16, help="Change the seed to generate different maps.")
parser.add_argument("--start", type=hex_int, default=0x77, help="Use hexcode 0xYX to pick a starting room. Y is top to bottom, 0 to F. X is left to right, 0 to F.")
parser.add_argument("--custom", type=str, default="none", help="provide a .csv (comma seperated values) file of a custom arrangement of the map screens")
parser.add_argument("--rom", type=str, default="none", help="provide a path to a ROM (.nes file) of Diggy Diggy Mole")

args = parser.parse_args()

seed = args.seed
start = args.start
custom = args.custom
rom = args.rom

random_state = seed

# Xorshift psuedorandom algorithm copied from https://en.wikipedia.org/wiki/Xorshift.
def random():
    global random_state
    random_state ^= random_state << 13
    random_state ^= random_state >> 17
    random_state ^= random_state << 5
    return random_state

rooms = [i for i in range(NUM_ROOMS)]

def swap(arr, i1, i2):
    temp = arr[i1]
    arr[i1] = arr[i2]
    arr[i2] = temp


if custom == "none":
    for i in range(len(rooms)):
        swap(rooms, i, random() & 0xFF )
else:
    rooms = np.genfromtxt(custom, delimiter=",", dtype=str, encoding="utf-8").flatten()
    rooms = [int("0xDD" if (room == "____") else room, 16) for room in rooms]


end1 = 0x06
end2 = 0xFE
dig = 0x83
down_drill = 0x45
up_drill = 0xBE
double_jump = 0x79
side_drill = 0x3C
title = 0x1D

start_new = start
end1_new = 0x00
end2_new = 0x00
dig_new = 0x00
down_drill_new = 0x00
up_drill_new = 0x00
double_jump_new = 0x00
side_drill_new = 0x00

title_new = 0x00
title_screen_exists = False

def hex_str(x):
    return format(x, '#04x')

out = "scramble = {\n"
for i in range(16):
    out += '\t'
    for j in range(16):
        curr_room = 16*i + j
        if rooms[curr_room] == end1:
            end1_new = curr_room
        if rooms[curr_room] == end2:
            end2_new = curr_room
        if rooms[curr_room] == dig:
            dig_new = curr_room
        if rooms[curr_room] == down_drill:
            down_drill_new = curr_room
        if rooms[curr_room] == up_drill:
            up_drill_new = curr_room
        if rooms[curr_room] == double_jump:
            double_jump_new = curr_room
        if rooms[curr_room] == side_drill:
            side_drill_new = curr_room
        if rooms[curr_room] == title:
            title_screen_exists = True
            title_new = curr_room

        out += hex_str(rooms[16*i + j]).upper()
        if not (i == 16 and j == 16):
            out += ", "
    out +='\n'
out += "}\n"
out += "start = " + hex_str(start_new).upper() + "\n"
out += "end1 = " + hex_str(end1_new).upper() + "\n"
out += "end2 = " + hex_str(end2_new).upper() + "\n"
out += "dig = " + hex_str(dig_new).upper() + "\n"
out += "down_drill = " + hex_str(down_drill_new).upper() + "\n"
out += "up_drill = " + hex_str(up_drill_new).upper() + "\n"
out += "double_jump = " + hex_str(double_jump_new).upper() + "\n"
out += "side_drill = " + hex_str(side_drill_new).upper() + "\n"
# print(out)

if rom == "none":
    #----------------------------------------------
    # Edit lua script
    #----------------------------------------------
    with open("ddm_randomizer.lua", "r+") as f:
        f.seek(0)
        f.write(out)
else:
    #----------------------------------------------
    # Edit DDM rom file (.nes file)
    #----------------------------------------------
    assert True == title_screen_exists, "The title screen (original map room 0x1D) must be present somewhere on the map"

    with open(rom, "rb") as f_old:
        rom_data = f_old.read()

        name = "../roms/"
        if custom == "none":
            name += "ddm_" + str(seed)
        else:
            # TODO parse custom map name and add to new rom file name
            name += (custom.split("/")[len(custom.split("/")) - 1]).split(".")[0]
            pass
        name += "_" + hex(start) + ".nes"

        with open(name, "wb+") as f_new:
            f_new.write(rom_data)

            f_new.seek(0x47d5) # which room contains the title screen
            f_new.write(title_new.to_bytes(1))

            f_new.seek(0x4a08)
            f_new.write(start_new.to_bytes(1))

            f_new.seek(0x7223) # address of the start of level data locations
            room_addrs_2 = f_new.read(0x100)
            room_addrs_2 = [room_addrs_2[i] for i in range(len(room_addrs_2))]
            room_addrs_2_new = [bytes(0) for i in range(len(room_addrs_2))]
            room_addrs_1 = f_new.read(0x100)
            room_addrs_1 = [room_addrs_1[i] for i in range(len(room_addrs_1))]
            room_addrs_1_new = [bytes(0) for i in range(len(room_addrs_1))]
            room_zones = f_new.read(0x100)
            room_zones = [room_zones[i] for i in range(len(room_zones))]
            room_zones_new = [bytes(0) for i in range(len(room_zones))]

            for i in range(NUM_ROOMS):
                room_addrs_2_new[i] = room_addrs_2[rooms[i]]
                room_addrs_1_new[i] = room_addrs_1[rooms[i]]
                room_zones_new[i] = room_zones[rooms[i]]

            f_new.seek(0x7223)
            f_new.write(bytes(room_addrs_2_new))
            f_new.write(bytes(room_addrs_1_new))
            f_new.write(bytes(room_zones_new))

#----------------------------------------------
# Generate new map image
#----------------------------------------------
from PIL import Image, ImageDraw
import numpy as np

old = np.array(Image.open("ddm_map_original.png"))
new = np.zeros((ROOM_HEIGHT*16, ROOM_WIDTH*16, 3), dtype=np.uint8)

for i in range(NUM_ROOMS):
    x = i // 16
    y = i % 16
    old_x = rooms[i] // 16
    old_y = rooms[i] % 16
    new[x*ROOM_HEIGHT:(x+1)*ROOM_HEIGHT, y*ROOM_WIDTH:(y+1)*ROOM_WIDTH] = old[old_x*ROOM_HEIGHT:(old_x+1)*ROOM_HEIGHT, old_y*ROOM_WIDTH:(old_y+1)*ROOM_WIDTH]

new = Image.fromarray(new)
new_draw = ImageDraw.Draw(new, mode="RGB")

def highlight_room(room, color):
    room_y = room // 16
    room_x = room % 16
    room_xy = [room_x*ROOM_WIDTH, room_y*ROOM_HEIGHT, (room_x + 1)*ROOM_WIDTH, (room_y + 1)*ROOM_HEIGHT]
    new_draw.rectangle(room_xy, outline=color, width=8)

def text_on_room(room, words):
    room_y = room // 16
    room_x = room % 16
    text_y = (room_y * ROOM_HEIGHT) + 120
    text_x = (room_x * ROOM_WIDTH) + 128
    new_draw.text((text_x, text_y), words, fill=(255, 255, 255), font_size=80, anchor="mm", align="center", stroke_width=3)

highlight_room(start_new, "white")
text_on_room(start_new, "START")
text_on_room(end1_new, "WIN 1")
text_on_room(end2_new, "WIN 2")
text_on_room(dig_new, "DIG")
text_on_room(down_drill_new, "DOWN\nDRILL")
text_on_room(up_drill_new, "UP\nDRILL")
text_on_room(double_jump_new, "DOUBLE\nJUMP")
text_on_room(side_drill_new, "SIDE\nDRILL")

new.save("ddm_map_randomized.png")