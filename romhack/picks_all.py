import picks_00, picks_01, picks_03, picks_07, picks_0f, picks_1f
from hack_rom import hack_da_rom
from classes import NUM_ROOMS, Map, Room, Sprite
from game_text import *

MAP_0F_START = 0x45
MAP_07_START = 0x3a
MAP_03_START = 0x8f
MAP_01_START = 0x96
MAP_00_START = 0xff

map = picks_1f.map

picks_0f.map.rooms[picks_0f.map.start] = None
picks_0f.map.shift(MAP_0F_START - 0x49)
map.merge(picks_0f.map)

picks_07.map.rooms[picks_07.map.start] = None
picks_07.map.shift(MAP_07_START - 0x41)
map.merge(picks_07.map)

picks_03.map.rooms[picks_03.map.start] = None
picks_03.map.shift(MAP_03_START - 0x42)
map.merge(picks_03.map)

picks_01.map.rooms[picks_01.map.start] = None
picks_01.map.shift(MAP_01_START - 0x42)
map.merge(picks_01.map)

picks_00.map.rooms[picks_00.map.start] = None
picks_00.map.shift(MAP_00_START - 0x50)
map.merge(picks_00.map)

# opening_scroll = OpeningScroll([
#     TextSpeed(1),
#     CursorPosition(0, 1),
#     Text('hey!'),
#     Pause(16),
#     Text('i\'m wondering if this works!'),
#     Pause(32),
#     CursorPosition(0, 3),
#     Text('yeah'),
#     TextSpeed(16),
#     Text('...'),
#     Pause(32),
#     TextSpeed(1),
#     Text('it does!'),
# ])

opening_scroll = CenteredIntroText([
    TextSpeed(5),
    Text('Whelp...'),
    Pause(15),
    NewLine(),
    TextSpeed(3),
    Text("Turns out the ancient dwarven cave I looted was taken over by a gang of librarians in the 60's."),
    Pause(15),
    NewLine(),
    NewLine(),
    Text("I got an email from 'em saying that if I didn't return those pickaxes I borrowed,"),
    Pause(9),
    Text("they'd borrow my kidneys"),
]).to_scroll()

pickaxe_text = PickaxeText(
    iron="yippee!\n\nyou returned the iron pick!",
    gold="hooray!\n\nyou returned the gold pick!",
    jade="huzzah!\n\nyou returned the jade pick!",
    opal="wowee!\n\nyou returned the opal pick!",
    ruby="tubular!\n\nyou returned the ruby pick!"
)

bytes_used = hack_da_rom(
    map,
    "../roms/ddm_pick_return.nes",
    "../roms/picks_all.nes",
    make_in_game_map=True,
    opening_scroll=opening_scroll,
    pickaxe_text=pickaxe_text
)

print("total bytes used: " + str(bytes_used))
print("bytes uncompressed: " + str(sum([240 for room in map.rooms if room != None])))