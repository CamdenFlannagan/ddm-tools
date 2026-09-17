scramble = {
	0XC, 0X1F, 0X7D, 0XBD, 0X6E, 0XE6, 0XA9, 0X51, 0X17, 0X5D, 0XB1, 0XE1, 0X28, 0X9E, 0X2B, 0XE0, 
	0X11, 0X1C, 0XEE, 0X7, 0X57, 0X6, 0X4D, 0X3C, 0XF4, 0XFF, 0XD4, 0X3E, 0X3D, 0X88, 0X2E, 0X60, 
	0XBB, 0X43, 0X46, 0X4B, 0X5B, 0X3B, 0X45, 0XB3, 0X13, 0XB8, 0XDA, 0XC6, 0X72, 0XE8, 0X39, 0X15, 
	0XD6, 0X44, 0X14, 0X3F, 0X7F, 0X67, 0X7C, 0X6F, 0XF2, 0XE3, 0X80, 0X90, 0XC3, 0X6D, 0XFE, 0X8D, 
	0XA1, 0XDF, 0X7A, 0XC7, 0X78, 0X2F, 0X62, 0XF5, 0X2D, 0XBE, 0X86, 0XCB, 0X18, 0X59, 0XAE, 0X4F, 
	0XF, 0X91, 0X22, 0X76, 0XAA, 0XEA, 0X37, 0XF9, 0XB5, 0X53, 0X58, 0XCE, 0X7E, 0XA5, 0X77, 0X20, 
	0X6B, 0X9A, 0X31, 0XD8, 0X85, 0XD1, 0X68, 0X4A, 0X75, 0XBF, 0XED, 0X92, 0X32, 0XA3, 0XD0, 0X8C, 
	0XBC, 0X84, 0X74, 0X2, 0X35, 0X94, 0XA7, 0X7B, 0X54, 0X64, 0XBA, 0XDC, 0X33, 0X52, 0X26, 0X0, 
	0XDB, 0XEB, 0X8F, 0X73, 0X87, 0XB9, 0X8A, 0X9, 0XC1, 0XFC, 0X38, 0X1A, 0XC9, 0XA0, 0XF3, 0XD, 
	0X82, 0XAF, 0X55, 0X5C, 0XFA, 0X9C, 0XF6, 0X79, 0XA4, 0XDE, 0X1D, 0X40, 0XFD, 0X48, 0X3A, 0X61, 
	0X30, 0XE7, 0X89, 0XB2, 0X81, 0X9B, 0XAC, 0X8E, 0X71, 0XAD, 0X99, 0X4C, 0X4, 0X19, 0X5A, 0XC0, 
	0XD9, 0X25, 0X97, 0X98, 0XD2, 0X70, 0XEF, 0XB, 0X9F, 0X69, 0XF8, 0XE, 0X1, 0X2A, 0X9D, 0XD5, 
	0X5E, 0X63, 0XB7, 0XFB, 0XA, 0XC5, 0XB4, 0XD3, 0XEC, 0X21, 0XCD, 0XE5, 0XF7, 0X42, 0X95, 0X4E, 
	0XF1, 0X83, 0XB0, 0XF0, 0X5F, 0X8, 0XE9, 0X12, 0X47, 0XAB, 0X3, 0X5, 0X6A, 0X1B, 0X2C, 0X36, 
	0XE2, 0XCC, 0XC8, 0X66, 0XC2, 0X6C, 0X10, 0XB6, 0X24, 0X16, 0XA8, 0X65, 0X41, 0XA2, 0X23, 0XC4, 
	0XA6, 0X27, 0X49, 0X50, 0X1E, 0X96, 0XCA, 0X34, 0XDD, 0X8B, 0XCF, 0X56, 0X93, 0XE4, 0XD7, 0X29, 
}
start = 0X88
end1 = 0X16
end2 = 0X3F
dig = 0XD2
down_drill = 0X27
up_drill = 0X4A
double_jump = 0X98
side_drill = 0X18

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
	emu.drawString(256 - (4 * 25), 240 - (8 * 1), "you are here: "..string.upper(string.format("%x", get_room())))
	-- I don't know why I need to add 1's here, but it makes it work I think lol
	--emu.drawString(0, 12, "goal: "..string.upper(string.format("%x", end1 + 1)).." or "..string.upper(string.format("%x", end2 + 1)))
end, emu.eventType.startFrame)

-- this should call just once around the beginning of each run
-- just setting an initial room value
emu.addMemoryCallback(function()
	--emu.write(0xC9F8, 0x88, emu.memType.nesMemory)
	set_room(0x88)
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


