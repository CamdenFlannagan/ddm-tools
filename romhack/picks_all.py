import picks_00, picks_01, picks_03, picks_07, picks_0f, picks_1f
from hack_rom import hack_da_rom
from classes import NUM_ROOMS, Map, Room, Sprite

MAP_0F_START = 0x45
MAP_07_START = 0x3a
MAP_03_START = 0x8f

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

bytes_used = hack_da_rom(map, "../roms/ddm_pick_return.nes", "../roms/picks_all.nes", make_in_game_map=True)

print("total bytes used: " + str(bytes_used))