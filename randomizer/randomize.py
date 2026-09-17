import random
import sys

if len(sys.argv) > 1:
    random.seed(int(sys.argv[1]))
else:
    random.seed(50)

rooms = [i for i in range(256)]

def swap(arr, i1, i2):
    temp = arr[i1]
    arr[i1] = arr[i2]
    arr[i2] = temp

for i in range(len(rooms)):
    swap(rooms, i, random.randint(0, 255))

end1 = 0x06
end2 = 0xFE
dig = 0x83
down_drill = 0x45
up_drill = 0xBE
double_jump = 0x79
side_drill = 0x3C

start_new = 0x88
end1_new = 0x00
end2_new = 0x00
dig_new = 0x00
down_drill_new = 0x00
up_drill_new = 0x00
double_jump_new = 0x00
side_drill_new = 0x00

out = "scramble = {\n"
for i in range(16):
    out += '\t'
    for j in range(16):
        curr_room = 16*i + j
        correction = (curr_room + 1) % 256
        if rooms[curr_room] == end1:
            end1_new = correction
        if rooms[curr_room] == end2:
            end2_new = correction
        if rooms[curr_room] == dig:
            dig_new = correction
        if rooms[curr_room] == down_drill:
            down_drill_new = correction
        if rooms[curr_room] == up_drill:
            up_drill_new = correction
        if rooms[curr_room] == double_jump:
            double_jump_new = correction
        if rooms[curr_room] == side_drill:
            side_drill_new = correction

        out += hex(rooms[16*i + j]).upper()
        if not (i == 16 and j == 16):
            out += ", "
    out +='\n'
out += "}\n"
out += "start = " + hex(start_new).upper() + "\n"
out += "end1 = " + hex(end1_new).upper() + "\n"
out += "end2 = " + hex(end2_new).upper() + "\n"
out += "dig = " + hex(dig_new).upper() + "\n"
out += "down_drill = " + hex(down_drill_new).upper() + "\n"
out += "up_drill = " + hex(up_drill_new).upper() + "\n"
out += "double_jump = " + hex(double_jump_new).upper() + "\n"
out += "side_drill = " + hex(side_drill_new).upper() + "\n"
# print(out)

with open("DDM Randomizer.lua", "r+") as f:
    f.seek(0)
    f.write(out)

from PIL import Image, ImageDraw
import numpy as np

old = np.array(Image.open("ddm_map_original.png"))
new = np.zeros((240*16, 256*16, 3), dtype=np.uint8)

for i in range(256):
    x = i // 16
    y = i % 16
    old_x = rooms[(i - 1) % 256] // 16
    old_y = rooms[(i - 1) % 256] % 16
    new[x*240:(x+1)*240, y*256:(y+1)*256] = old[old_x*240:(old_x+1)*240, old_y*256:(old_y+1)*256]

new = Image.fromarray(new)
new_draw = ImageDraw.Draw(new, mode="RGB")
new_draw.ink = 255

def highlight_room(room, color):
    room_y = room // 16
    room_x = room % 16
    room_xy = [room_x*256, room_y*240, (room_x + 1)*256, (room_y + 1)*240]
    new_draw.rectangle(room_xy, outline=color, width=8)

def text_on_room(room, words):
    room_y = room // 16
    room_x = room % 16
    text_y = (room_y * 240) + 120
    text_x = (room_x * 256) + 128
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