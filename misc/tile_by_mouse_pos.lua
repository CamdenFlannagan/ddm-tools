
function hex(num)
	return string.format("%X", num)
end

emu.addEventCallback(function()

	mouse = emu.getMouseState()
	
	emu.drawString(0,0,"x, y: " .. hex(mouse.x // 16) .. ", " .. hex(mouse.y // 16))

end, emu.eventType.startFrame)