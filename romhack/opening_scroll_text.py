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

    def __str__(self):
        return 'Pause(' + str(self.x) + ')'

class TextSpeed:
    def __init__(self, x: int):
        assert x >= 0 and x < 256, "text speed argument must be 1 byte"
        self.x = x

    def to_bytes(self):
        return b'\x81' + self.x.to_bytes(1)

    def __str__(self):
        return 'TextSpeed(' + str(self.x) + ')'

class CursorPosition:
    '''
    place the cursor at tile x, y (tiles are 8 by 8 pixel squares)
    '''
    def __init__(self, x: int, y: int):
        assert x >= 0 and x < 32, 'you tried ' + str(x)
        assert y >= 0 and y < 30, 'you tried ' + str(y)
        self.x = x
        self.y = y

    def to_bytes(self):
        return b'\x7e' + (0x2000 + 32*self.y + self.x).to_bytes(2, 'big')

    def __str__(self):
        return 'CursorPosition(' + str(self.x) + ', ' + str(self.y) + ')'

class Text:
    def __init__(self, text: str):
        self.text = text.upper()

    def to_bytes(self):
        return self.text.encode(encoding='ascii')

    def __str__(self):
        return 'Text(' + self.text + ')'



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

    def __str__(self):
        return str([str(command) for command in self.commands])


'''
automatically center text for convenience.
use the NewLine class for new lines instead of using CursorPosition.
the text will automatically move to a new line if it gets longer than the maximum width
'''

MAX_WIDTH = 28

class NewLine: # lol ¯\_(ツ)_/¯ it works
    pass

class CenteredIntroText:
    def __init__(self, commands: list[ Pause | TextSpeed | NewLine | Text ]):
        self.commands = commands

    def to_scroll(self):

        inter = [] # intermediate structure to make transition from input to scroll simpler
        full_msg = ''

        # make the structure
        for command in self.commands:
            if isinstance(command, Text):
                for char in command.text:
                    full_msg += char
        i = 0
        inter = [[] for j in range(len(full_msg))]
        for command in self.commands:
            if isinstance(command, Text):
                for char in command.text:
                    i += 1
            else:
                inter[i].append(command)

        # add cursor position commands
        i = 0
        curr_line_len = 0
        inter[0].append(CursorPosition(0, 0)) # first text always needs cursor position
        while i < len(full_msg):
            for j in range(len(inter[i])):
                if isinstance(inter[i][j], NewLine):
                    inter[i][j] = CursorPosition(0, 0)
                    curr_line_len = 0
            if curr_line_len >= MAX_WIDTH:
                while full_msg[i] != ' ':
                    i -= 1
                inter[i].append(CursorPosition(0, 0))
                curr_line_len = 0
            else:
                curr_line_len += 1

            i += 1

        def contains_instance(stuff: list, what_is_it: type):
            for thing in stuff:
                if isinstance(thing, what_is_it):
                    return True
            return False

        def num_instances(stuff: list, what_is_it: type):
            count = 0
            for thing in stuff:
                if isinstance(thing, what_is_it):
                    count += 1
            return count

        # set all the cursor positions
        line_num = 0
        for i in range(len(full_msg)):
            for j in range(len(inter[i])):
                if isinstance(inter[i][j], CursorPosition):
                    # then set CurPos's x and y based on how far away the next CurPos is
                    # exclude spaces on edges of lines
                    look_ahead = i + 1
                    while look_ahead < len(full_msg):
                        if contains_instance(inter[look_ahead], CursorPosition):
                            break
                        look_ahead += 1
                    line_len = look_ahead - i - (1 if full_msg[i] == ' ' else 0)

                    inter[i][j].x = 16 - (line_len // 2)
                    inter[i][j].y = 2 + 2*line_num

                    line_num += 1

        # add text and make scroll!        
        scroll: list[ CursorPosition | TextSpeed | Pause | Text ] = []
        i = 0
        while i < len(full_msg):
            if len(inter[i]) > 0:
                for command in inter[i]:
                    scroll.append(command)
                
                skip_space = 0
                if contains_instance(inter[i], CursorPosition) and full_msg[i] == ' ':
                    skip_space = 1

                start = i
                i += 1
                while i < len(full_msg) and len(inter[i]) == 0:
                    i += 1

                scroll.append(Text(full_msg[start + skip_space : i]))
            else:
                i += 1

        return OpeningScroll(scroll)

'''
Messages for getting a pickaxe
60 xx yy <-- Place the cursor at pixel xx, yy
'''