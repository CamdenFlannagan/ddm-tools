
function hex(num)
	return string.format("%X", num)
end

emu.addEventCallback(function()

	mouse = emu.getMouseState()
	if mouse.left then
		x = mouse.x // 16
		y = mouse.y // 16
		
		-- draw x and y position of mouse
		emu.drawString(0,0,"x, y: " .. hex(x) .. ", " .. hex(y))
		
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