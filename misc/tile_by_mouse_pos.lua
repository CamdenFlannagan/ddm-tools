
function hex(num)
	return string.format("%X", num)
end

emu.addEventCallback(function()

	mouse = emu.getMouseState()
	if mouse.left then
		--emu.drawString(0,16, "true x, y"..mouse.x.." "..mouse.y)
	
		x = mouse.x // 16
		y = mouse.y // 16
		
		-- draw x and y position of mouse
		emu.drawString(0,0,"x, y: " .. hex(x) .. ", " .. hex(y))
		
		-- draw tile hexcode
		tile = emu.read(0x400 + (y*2*2*2*2 + x), emu.memType.nesMemory)
		tile_str = hex(tile)
		if tile < 16 then
			tile_str = "0"..tile_str
		end
		emu.drawString(0,8, tile_str)
		
		-- draw box around tile
		emu.drawLine( 16*x-1,   16*y-1,   16*(x+1), 16*y-1   )
		emu.drawLine( 16*(x+1), 16*y-1,   16*(x+1), 16*(y+1) )
		emu.drawLine( 16*(x+1), 16*(y+1), 16*x-1,   16*(y+1) )
		emu.drawLine( 16*x-1,   16*(y+1), 16*x-1,   16*y-1   )
	else
		emu.drawString(0,0,"click on tile...")
	end
	
	-- print room number
	emu.drawString(0, 14*16, "room: "..hex(emu.read(0x48, emu.memType.nesInternalRam)))

end, emu.eventType.startFrame)