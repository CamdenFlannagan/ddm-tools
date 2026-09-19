scramble = {
	0X78, 0XEE, 0X99, 0X75, 0XA7, 0XDC, 0X2E, 0XF3, 0X0, 0XC2, 0XB2, 0XBA, 0X6F, 0XB, 0X1, 0X9B, 
	0X9F, 0X65, 0X5C, 0X51, 0XA, 0X72, 0X76, 0XD0, 0X18, 0X25, 0XAD, 0X57, 0X45, 0XA4, 0X1B, 0X8B, 
	0X7B, 0X6E, 0X5D, 0X41, 0X98, 0X55, 0X71, 0X35, 0X2B, 0X3F, 0XAB, 0X7F, 0X90, 0X52, 0X70, 0X43, 
	0X46, 0X61, 0X27, 0X6C, 0X2A, 0XAE, 0XEB, 0X4A, 0X60, 0XE6, 0X6D, 0X80, 0XF6, 0X5E, 0XB3, 0X8E, 
	0XE1, 0XC7, 0X94, 0XC5, 0XAC, 0X93, 0X17, 0XC4, 0X7E, 0XD4, 0X8F, 0XE9, 0XD, 0XBF, 0X7, 0XD8, 
	0X26, 0X3E, 0X8D, 0XBB, 0X29, 0X5, 0XFA, 0X86, 0XDB, 0X7C, 0X33, 0X4F, 0X63, 0X10, 0X88, 0X7D, 
	0XDF, 0X14, 0X6, 0X3A, 0X47, 0X23, 0X32, 0X1E, 0X4C, 0X20, 0X2D, 0XB4, 0X97, 0X79, 0X8A, 0XB7, 
	0XAA, 0X91, 0X84, 0XC3, 0X16, 0X9C, 0XCC, 0X56, 0XE, 0X6B, 0XBC, 0XA3, 0X44, 0X4D, 0X7A, 0X1F, 
	0X92, 0XF2, 0X2C, 0XFB, 0XE4, 0XD2, 0XD7, 0XBE, 0X37, 0X30, 0XB8, 0XA5, 0X73, 0X40, 0XDD, 0X58, 
	0X74, 0X82, 0X12, 0XFC, 0X4, 0X9A, 0XC6, 0XB0, 0XE7, 0XA1, 0X64, 0X24, 0X48, 0X3C, 0XCA, 0XB1, 
	0X4B, 0X9E, 0XD3, 0XA8, 0XD1, 0XD6, 0X95, 0XA2, 0XCF, 0XC1, 0XEA, 0XEC, 0X2F, 0XCB, 0X15, 0X8, 
	0X22, 0XCD, 0X5F, 0XFE, 0X77, 0XF5, 0X87, 0X34, 0X69, 0XF9, 0X21, 0X49, 0X11, 0XC0, 0X4E, 0X28, 
	0XA0, 0XAF, 0X42, 0XEF, 0XF8, 0XF1, 0XB5, 0XC9, 0X8C, 0XE2, 0XE5, 0XDA, 0XB9, 0X2, 0X9, 0XDE, 
	0X67, 0XF, 0X3B, 0X31, 0X96, 0X1A, 0XA9, 0X81, 0X68, 0XF0, 0X36, 0X19, 0XFD, 0X38, 0XF7, 0X62, 
	0XE0, 0XCE, 0X85, 0X66, 0XF4, 0XD5, 0XC8, 0XD9, 0X13, 0X9D, 0X54, 0XFF, 0X83, 0XB6, 0X1D, 0X53, 
	0XE3, 0X5B, 0X3, 0XE8, 0X50, 0X59, 0X3D, 0X1C, 0XA6, 0X6A, 0X39, 0X5A, 0XBD, 0XC, 0X89, 0XED, 
}
start = 0X77
end1 = 0X63
end2 = 0XB4
dig = 0XED
down_drill = 0X1D
up_drill = 0X88
double_jump = 0X6E
side_drill = 0X9E

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


