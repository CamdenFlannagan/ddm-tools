from enum import Enum


'''
Opening Scroll Text Commands
80 xx    <-- Pause for some f of xx
81 xx    <-- Type text at a rate of some f of xx
7e 2x xx <-- Move the text cursor to xxx (the 2 may be something idk)
00       <-- End
'''

class Pause:
    def __init__(self, x: int):
        assert x >= 0 and x < 256, "pause argument must be 1 byte"
        self.x = x

    def to_bytes(self):
        return b'\x80' + self.x.to_bytes(1)

class TextSpeed:
    def __init__(self, x: int):
        assert x >= 0 and x < 256, "text speed argument must be 1 byte"
        self.x = x

    def to_bytes(self):
        return b'\x81' + self.x.to_bytes(1)

class CursorPosition:
    '''
    place the cursor at tile x, y (tiles are 8 by 8 pixel squares)
    '''
    def __init__(self, x: int, y: int):
        assert x >= 0 and x < 32
        assert y >= 0 and y < 30
        self.x = x
        self.y = y

    def to_bytes(self):
        return b'\x7e' + (0x2000 + 32*self.y + self.x).to_bytes(2, 'big')

class Text:
    def __init__(self, text: str):
        self.text = text.upper()

    def to_bytes(self):
        return self.text.encode(encoding='ascii')



MAX_OPENING_SCROLL_LEN = 0x159

class OpeningScroll:
    def __init__(self, commands: list[ Pause | TextSpeed | CursorPosition | Text ]):
        self.commands = commands

    def to_bytes(self):
        out = b''
        for command in self.commands:
            out += command.to_bytes()
        out += b'\x00'
        assert len(out) <= MAX_OPENING_SCROLL_LEN, 'opening scroll must use fewer than ' + MAX_OPENING_SCROLL_LEN + ' bytes'
        return out

'''
def line_it_up_bro(text):
    assert len(text) <= MAX_WIDTH, "less than 28 chars per line please"
    x = 16 - (len(text) // 2)
    y = 2 + 2*line_num

    scroll.append(CursorPosition(x, y))
    scroll.append(Text(text))
    
    line_num += 1
'''

'''
automatically center text for convenience.
use the \n (newline) character for new lines instead of using CursorPosition.
the text will automatically move to a new line if it gets longer than the maximum width
'''
MAX_WIDTH = 28
class CenteredIntroText:
    def __init__(self, commands: list[ Pause | TextSpeed | Text ]):
        self.commands = commands

    def to_bytes(self):
        scroll: list[ Pause | TextSpeed | CursorPosition | Text ] = []

        curr_line_num = 0
        curr_line_length = 0
        curr_text_segment = ''
        commands_waiting_to_be_pooped = []

        # yada yada yada
        for command in self.commands:
            if command.isinstance(Pause):
                commands_waiting_to_be_pooped.append(command)

            if command.isinstance(TextSpeed):
                commands_waiting_to_be_pooped.append(command)

        return OpeningScroll(scroll).to_bytes()

'''
Pickaxe Get Messages
60 xx yy <-- Place the cursor at pixel xx, yy
'''