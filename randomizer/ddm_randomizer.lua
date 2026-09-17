scramble = {
	0X31, 0X53, 0XEF, 0X9E, 0XAB, 0X54, 0XA5, 0X2D, 0X12, 0X5E, 0X9C, 0X48, 0X34, 0X4B, 0X24, 0X8B, 
	0XDA, 0XA7, 0X40, 0X93, 0X11, 0X72, 0X30, 0XD8, 0X32, 0X5D, 0XE5, 0XD, 0X27, 0X37, 0X35, 0XE2, 
	0X4, 0XC3, 0XA2, 0X45, 0X44, 0XB3, 0X9D, 0XC9, 0X20, 0X23, 0X58, 0X4F, 0X38, 0X2C, 0XFA, 0XF, 
	0XF7, 0X15, 0X6D, 0XF3, 0X66, 0XD2, 0XCD, 0X0, 0X91, 0X57, 0X10, 0X71, 0X6B, 0X4E, 0X17, 0XE7, 
	0X73, 0X76, 0X7D, 0X85, 0XD7, 0X33, 0XBF, 0XCB, 0XCE, 0XEC, 0X86, 0X8D, 0X5, 0XE4, 0XA1, 0X5B, 
	0X65, 0X97, 0X19, 0X26, 0X89, 0XA3, 0X7B, 0XB5, 0XB7, 0X4C, 0X3E, 0X2E, 0X25, 0X67, 0X83, 0X6C, 
	0XAA, 0X77, 0XBC, 0X3F, 0XFC, 0XA, 0XB1, 0X9B, 0XFB, 0XAE, 0X3C, 0X3D, 0XE0, 0XC7, 0X64, 0XA9, 
	0XE, 0X59, 0X92, 0X8E, 0X39, 0X88, 0X78, 0X99, 0XCC, 0XF1, 0X7F, 0XEA, 0XBA, 0X2A, 0XB6, 0X1F, 
	0XE3, 0X1B, 0X2, 0XC4, 0XC8, 0X7E, 0X6E, 0XA4, 0XE1, 0X42, 0XEB, 0X14, 0XBB, 0X22, 0X74, 0XF2, 
	0X5C, 0XDF, 0XFD, 0XB8, 0X6F, 0X7A, 0XD0, 0X55, 0XAF, 0X98, 0XB4, 0X9A, 0X7C, 0X21, 0X2B, 0X8A, 
	0XDD, 0XD3, 0X46, 0X90, 0XF4, 0XFF, 0XF0, 0XC, 0XC2, 0X87, 0X80, 0XB0, 0X3B, 0X18, 0X69, 0X28, 
	0XD9, 0XDB, 0X16, 0X4A, 0X95, 0XD5, 0X13, 0XC6, 0X94, 0XC0, 0X4D, 0X75, 0XCF, 0XDE, 0XA8, 0XB, 
	0XC1, 0X50, 0XF9, 0XCA, 0X2F, 0X47, 0X8C, 0X41, 0X70, 0X1D, 0X56, 0X1, 0X62, 0XAD, 0X6A, 0XD1, 
	0X6, 0X79, 0X29, 0XED, 0XF8, 0XBD, 0XD6, 0XD4, 0XBE, 0XEE, 0X68, 0XFE, 0XA6, 0XB2, 0XB9, 0X1A, 
	0X84, 0X52, 0X43, 0XF6, 0XF5, 0X51, 0X3, 0XE6, 0XDC, 0X61, 0XE8, 0X5F, 0X1E, 0X63, 0XA0, 0X82, 
	0X1C, 0XE9, 0X5A, 0X60, 0X49, 0X9F, 0X81, 0X8F, 0X3A, 0X7, 0X8, 0X96, 0X36, 0XAC, 0X9, 0XC5, 
}
start = 0X77
end1 = 0XD1
end2 = 0XDC
dig = 0X5F
down_drill = 0X24
up_drill = 0XD9
double_jump = 0XD2
side_drill = 0X6B

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
	set_room(start)
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


