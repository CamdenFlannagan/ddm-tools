scramble = {
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0X70, 0X06, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0X80, 0X81, 0X82, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0X90, 0X91, 0X92, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
	0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 0XDD, 
}
start = 0X77
end1 = 0X58
end2 = 0X00
dig = 0X00
down_drill = 0X00
up_drill = 0X00
double_jump = 0X00
side_drill = 0X00
0



room_addr = 0x2F0 -- this addr seemed unused by the game, so I'm using it to store where we are
function get_room()
	return emu.read(room_addr, emu.memType.nesInternalRam, false)
end
function set_room(room_num)
	emu.write(room_addr, room_num, emu.memType.nesInternalRam)
end
function goto_room(room_num)
	emu.write(0x48, room_num, emu.memType.nesInternalRam)
end

emu.addMemoryCallback(function()
	goto_room(scramble[get_room()])
end,
emu.callbackType.write,
0x0041, 0x0041,
emu.cpuType.nes,
emu.memType.nesMemory)

-- yo, where are we?
emu.addEventCallback(function()
	--emu.drawString(256 - (4 * 25), 240 - (8 * 1), "you are here: "..string.upper(string.format("%x", get_room())))
	-- I don't know why I need to add 1's here, but it makes it work I think lol
	--emu.drawString(0, 12, "goal: "..string.upper(string.format("%x", end1 + 1)).." or "..string.upper(string.format("%x", end2 + 1)))
end, emu.eventType.startFrame)

-- this should call just once around the beginning of each run
-- just setting an initial room value
emu.addMemoryCallback(function()
	set_room((start + 1) % 256) -- idk why i need to add 1, but it works lol
end,
emu.callbackType.exec,
0xD46D, 0xD46D,
emu.cpuType.nes,
emu.memType.nesMemory)

-- detect left transition
emu.addMemoryCallback(function()
	set_room((get_room() - 0x01) % 256)
end,
emu.callbackType.exec,
0x9885, 0x9885,
emu.cpuType.nes,
emu.memType.nesMemory)

-- detect right transition
emu.addMemoryCallback(function()
	set_room((get_room() + 0x01) % 256)
end,
emu.callbackType.exec,
0x98B2, 0x98B2,
emu.cpuType.nes,
emu.memType.nesMemory)

-- detect up transition
emu.addMemoryCallback(function()
	set_room((get_room() - 0x10) % 256)
end,
emu.callbackType.exec,
0x9830, 0x9830,
emu.cpuType.nes,
emu.memType.nesMemory)

-- detect down transition
emu.addMemoryCallback(function()
	set_room((get_room() + 0x10) % 256)
end,
emu.callbackType.exec,
0x985E, 0x985E,
emu.cpuType.nes,
emu.memType.nesMemory)


