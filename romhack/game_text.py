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
                # people can add commands after their final text, but there's
                # no reason to cause they wouldn't have any observable effects.
                # so I'm just going to pretend they don't exist
                if i < len(inter):
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
        from math import ceil
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

                    inter[i][j].x = 16 - ceil(line_len / 2)
                    inter[i][j].y = 2 + 2*line_num

                    line_num += 1

        # print([(full_msg[i], inter[i]) for i in range(len(full_msg))])
        
        # add text and make scroll!        
        scroll: list[ CursorPosition | TextSpeed | Pause | Text ] = []
        i = 0
        while i < len(full_msg):
            if len(inter[i]) > 0:
                # add all commands but add only the FINAL cursor position command per group
                cursor_poses = num_instances(inter[i], CursorPosition)
                cursor_pos = 1
                for command in inter[i]:
                    if isinstance(command, CursorPosition):
                        if cursor_pos == cursor_poses:
                            scroll.append(command)
                        cursor_pos += 1
                    else:
                        scroll.append(command)

                # figure out the text command
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

from addresses import *

class PickaxeText:     
    def __init__(self, iron: str, gold: str, jade: str, opal: str, ruby: str):
        self.iron = self._PickaxeText(iron, IRON_TEXT_LEN)
        self.gold = self._PickaxeText(gold, GOLD_TEXT_LEN)
        self.jade = self._PickaxeText(jade, JADE_TEXT_LEN)
        self.opal = self._PickaxeText(opal, OPAL_TEXT_LEN)
        self.ruby = self._PickaxeText(ruby, RUBY_TEXT_LEN)

    def to_bytes(self):
        out = b''
        out += self.iron.to_bytes()
        out += self.gold.to_bytes()
        out += self.jade.to_bytes()
        out += self.opal.to_bytes()
        out += self.ruby.to_bytes()
        return out
    
    class _PickaxeText:
        '''
        60 xx yy <-- Place the cursor at pixel xx, yy
        '''
        class PixelPosition:
            def __init__(self, x: int, y: int):
                self.x = x
                self.y = y

            def to_bytes(self):
                return b'\x60' + self.x.to_bytes(1) + self.y.to_bytes(1)
            
        def __init__(self, text: str, max_len: int):
            self.text = text
            self.max_len = max_len

        def to_bytes(self):
            MAX_WIDTH = 80    # maximum line width in pixels
            CHAR_WIDTH = 8    # width of a character in pixels
            CHAR_HEIGHT = 16  # height of character in pixels

            SCREEN_WIDTH = 0x100  # width of the screen in pixels
            SCREEN_HEIGHT = 0xF0  # height of the screen in pixels

            lines: str = []

            i = 0
            while i < len(self.text):
                txt = ''

                start = i
                while i < len(self.text):
                    line_len = i - start
                    if self.text[i] == '\n':
                        break
                    if CHAR_WIDTH*line_len >= MAX_WIDTH:
                        while self.text[i] != ' ':
                            i -= 1
                        break
                    i += 1

                line = self.text[start : i]
                lines.append(line)

                i += 1
            
            out = b''

            center_width = SCREEN_WIDTH // 2
            center_height = SCREEN_HEIGHT // 2

            msg_y_start = center_height - ((len(lines)*CHAR_HEIGHT) // 2)

            print(lines)
            
            for line_num, line in enumerate(lines):
                if line == '': # no need to add bytes for empty lines!
                    continue
                out += self.PixelPosition(
                    center_width - ((CHAR_WIDTH*len(line)) // 2),
                    msg_y_start + (CHAR_HEIGHT*line_num)
                ).to_bytes()
                out += line.encode(encoding='ascii')

            assert len(out) + 1 <= self.max_len # + 1 because we still need to add at least one b'\x00'
            out += b'\x00' * (self.max_len - len(out))
            return out

# PickaxeTexts.PickaxeText("I like\nwearing jeans on sundays", 0x3e).to_bytes()