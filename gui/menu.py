import tcod
import settings
import pyfiglet
import time
import os
import textwrap
from os.path import isfile
from game.util.constants import Palette
from game.util.fs import savefile_exists
from game.util import constants
from game.util.text import DocumentWrapper

class MainMenu(object):
    def __init__(self, console):
        self.title = pyfiglet.figlet_format("ZONA", font="slant")
        self.console = console
        self.cursorposX = 28
        self.cursorposY = 20
        self.menu_select = "new game"
        self.continue_muted = not savefile_exists()

    def draw_title(self):
        tcod.console_set_default_foreground(self.console, tcod.magenta)
        tcod.console_print(self.console, 24, 2, self.title)
        tcod.console_set_default_foreground(self.console, tcod.cyan)
        tcod.console_print(self.console, 26, 4, self.title)
        tcod.console_set_default_foreground(self.console, tcod.yellow)
        tcod.console_print(self.console, 28, 6, self.title)

    def draw_options(self):
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_print(self.console, 36, 20, "New game")
        if self.continue_muted:
            tcod.console_set_default_foreground(self.console, tcod.dark_gray)
        tcod.console_print(self.console, 36, 24, "Continue")
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_print(self.console, 36, 28, "Settings")
        tcod.console_print(self.console, 38, 32, "Exit")

    def draw_cursor(self):
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, tcod.CHAR_ARROW2_E, tcod.BKGND_NONE)

    def cursor_down(self):
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, " ", tcod.BKGND_NONE)
        self.cursorposY += 4
        if self.cursorposY < 33:
            pass
        else:
            self.cursorposY = 20

        if self.menu_select == "new game":
            self.menu_select = "continue"
        elif self.menu_select == "continue":
            self.menu_select = "settings"
        elif self.menu_select == "settings":
            self.menu_select = "exit"
        elif self.menu_select == "exit":
            self.menu_select = "new game"

    def cursor_up(self):
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, " ", tcod.BKGND_NONE)
        self.cursorposY -= 4
        if self.cursorposY > 19:
            pass
        else:
            self.cursorposY = 32

        if self.menu_select == "new game":
            self.menu_select = "exit"
        elif self.menu_select == "continue":
            self.menu_select = "new game"
        elif self.menu_select == "settings":
            self.menu_select = "continue"
        elif self.menu_select == "exit":
            self.menu_select = "settings"


class SettingsMenu(object):
    def __init__(self, console):
        self.state = "settings_select"
        self.menu_select = "delete_save_file"
        self.cursorposX = 5
        self.cursorposY = 4
        self.console = console
        self.delete_save_muted = not savefile_exists()
        self.delete_save = False

    def cursor_down(self):
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, " ", tcod.BKGND_NONE)
        self.cursorposY += 2
        if self.cursorposY < 11:
            pass
        else:
            self.cursorposY = 4

        if self.menu_select == "delete_save_file":
            self.menu_select = "set_character_map"
        elif self.menu_select == "set_character_map":
            self.menu_select = "auto_checkpoint"
        elif self.menu_select == "auto_checkpoint":
            self.menu_select = "back"
        elif self.menu_select == "back":
            self.menu_select = "delete_save_file"

    def cursor_up(self):
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, " ", tcod.BKGND_NONE)
        self.cursorposY -= 2
        if self.cursorposY > 3:
            pass
        else:
            self.cursorposY = 10

        if self.menu_select == "delete_save_file":
            self.menu_select = "back"
        elif self.menu_select == "set_character_map":
            self.menu_select = "delete_save_file"
        elif self.menu_select == "auto_checkpoint":
            self.menu_select = "set_character_map"
        elif self.menu_select == "back":
            self.menu_select = "auto_checkpoint"

    def draw_cursor(self):
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, tcod.CHAR_ARROW2_E, tcod.BKGND_NONE)

    def draw_checkbox(self):
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_put_char(self.console, 26, 8, constants.CP437_CHAR_BULLET_SQUARE)

    def draw_options(self):
        tcod.console_set_default_foreground(self.console, tcod.white)

        tcod.console_print(self.console, 10, 6, "Set character map")
        tcod.console_print(self.console, 10, 8, "Auto checkpoint")
        tcod.console_print(self.console, 10, 10, "Back")

        if self.delete_save_muted:
            tcod.console_set_default_foreground(self.console, tcod.dark_grey)
        tcod.console_print(self.console, 10, 4, "Delete save file")

    def delete_save_file(self):
        file = settings.USER_DIR + "/save.db"
        if isfile(file):
            os.remove(file)
            self.delete_save = False
            self.delete_save_muted = not savefile_exists()

class ConfirmationMenu(object):
    def __init__(self, console, message, x, y, w, h, title=None, message_color=tcod.white, bg_color=tcod.black,
                 border_color=tcod.white, title_color=tcod.white):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.message_color = message_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.title_color = title_color
        self.console = console
        wrapper = DocumentWrapper(width=(self.w - self.x) - 2)
        self.message = wrapper.wrap(text=message)
        self.state = "hidden"

    def draw_confirmation(self):

        for i in range(self.x, self.w):
            for j in range(self.y, self.h):
                tcod.console_set_char_background(self.console, i, j, self.bg_color, tcod.BKGND_SET)
                tcod.console_put_char(self.console, i, j, " ")

        for i in range(0, self.w - self.x):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i + self.x, self.y, tcod.CHAR_HLINE)

        for i in range(0, self.w - self.x):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i + self.x, self.h, tcod.CHAR_HLINE)

        for i in range(0, self.h - self.y):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.x, i + self.y, tcod.CHAR_VLINE)

        for i in range(0, self.h - self.y):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.w, i + self.y, tcod.CHAR_VLINE)

        tcod.console_set_default_foreground(self.console, self.border_color)
        tcod.console_put_char(self.console, self.w, self.y, tcod.CHAR_NE)
        tcod.console_put_char(self.console, self.w, self.h, tcod.CHAR_SE)
        tcod.console_put_char(self.console, self.x, self.y, tcod.CHAR_NW)
        tcod.console_put_char(self.console, self.x, self.h, tcod.CHAR_SW)

        message_margin = 0
        for line in self.message:
            message_margin = max(message_margin, len(line))
        mmarginX = ((self.w - self.x) - message_margin) / 2
        mmarginX = int(self.x + mmarginX)
        title_margin = len(self.title)
        tmarginX = ((self.w - self.x) - title_margin) / 2
        tmarginX = int(self.x + tmarginX)
        if len(self.message) > 1:
            marginY = self.y + 2
        else:
            marginY = int(((self.h - self.y) / 2) + self.y)

        tcod.console_set_default_foreground(self.console, self.message_color)
        msgy = 0

        for line in self.message:
            x = 0
            if len(line) < message_margin:
                x = int((len(line) / 2) + mmarginX)
            else:
                x = mmarginX
            tcod.console_print(self.console, x, marginY + msgy, line)
            msgy += 1
        if self.title is not None:
            tcod.console_set_default_foreground(self.console, self.title_color)
            tcod.console_print(self.console, tmarginX, self.y, self.title)


class SelectionMenu(object):
    def __init__(self, console, selections, x, y, w, h, title=None, selection_color=tcod.white, bg_color=tcod.black,
                 border_color=tcod.white, title_color=tcod.white, cursor_color=tcod.white):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = "/ " + title + " /"
        self.selection_color = selection_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.title_color = title_color
        self.cursor_color = cursor_color
        self.console = console
        self.selections = selections
        self.menu_select = 0
        max_selections = 8
        self.selection_count = max_selections
        if len(selections) < self.selection_count:
            self.selection_count = len(selections)
        self.selection_start = 0
        self.selection_end = 4
        if self.selection_count < self.selection_end:
            self.selection_end = self.selection_count

        self.logical_position = 0
        self.logical_max = self.selection_end - 1
        self.cursorposX = self.x + 2
        self.cursorposY = self.y + 2

    def cursor_down(self):
        if self.menu_select < (self.selection_count - 1):
            self.menu_select += 1
        if self.logical_position < self.logical_max:
            self.logical_position += 1
            self.cursorposY += 2
        else:
            if self.selection_end < self.selection_count:
                self.selection_start += 1
                self.selection_end += 1

    def cursor_up(self):
        if self.menu_select > 0:
            self.menu_select -= 1
        if self.logical_position > 0:
            self.logical_position -= 1
            self.cursorposY -= 2
        else:
            if self.selection_start > 0:
                self.selection_start -= 1
                self.selection_end -= 1

    def draw_cursor(self):
        tcod.console_set_default_foreground(self.console, self.cursor_color)
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, tcod.CHAR_ARROW2_E, tcod.BKGND_NONE)

    def draw_window(self):
        for i in range(self.x, self.w):
            for j in range(self.y, self.h):
                tcod.console_set_char_background(self.console, i, j, self.bg_color, tcod.BKGND_SET)
                tcod.console_put_char(self.console, i, j, " ")

        for i in range(self.x, self.w):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.y, tcod.CHAR_HLINE)

        for i in range(self.x, self.w):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.h, tcod.CHAR_HLINE)

        for i in range(self.y, self.h):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.x, i, tcod.CHAR_VLINE)

        for i in range(self.y, self.h):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.w, i, tcod.CHAR_VLINE)

        tcod.console_set_default_foreground(self.console, self.border_color)
        tcod.console_put_char(self.console, self.w, self.y, tcod.CHAR_NE)
        tcod.console_put_char(self.console, self.w, self.h, tcod.CHAR_SE)
        tcod.console_put_char(self.console, self.x, self.y, tcod.CHAR_NW)
        tcod.console_put_char(self.console, self.x, self.h, tcod.CHAR_SW)
        tcod.console_put_char(self.console, self.w, self.y + 1, tcod.CHAR_ARROW_N)
        tcod.console_put_char(self.console, self.w, self.h - 1, tcod.CHAR_ARROW_S)

        title_margin = len(self.title)
        tmarginX = ((self.w - self.x) - title_margin) / 2
        tmarginX = int(self.x + tmarginX)
        marginY = int(((self.h - self.y) / 2) + self.y)
        if self.title is not None:
            tcod.console_set_default_foreground(self.console, self.title_color)
            tcod.console_print(self.console, tmarginX, self.y, self.title)

    def draw_options(self):
        logical_selections = self.selections[self.selection_start:self.selection_end]
        posX = 4 + self.x
        posY = 0 + self.y
        for selection in logical_selections:
            posY += 2
            tcod.console_set_default_foreground(self.console, self.selection_color)
            tcod.console_print(self.console, posX, posY, selection)


class InputMenu(object):
    def __init__(self, console, x, y, w, h, title=None, message=None, cursor_color=tcod.white, input_color=tcod.white,
                 message_color=tcod.white, border_color=tcod.white, title_color=tcod.white, bg_color=tcod.black):
        self.console = console
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.message = message
        self.input = []
        self.viewport = []
        self.viewport_start = 0
        self.viewport_max = self.w - self.x - 4
        self.viewport_end = self.viewport_max
        self.input_logical = []
        self.cursor_color = cursor_color
        self.input_color = input_color
        self.border_color = border_color
        self.message_color = message_color
        self.bg_color = bg_color
        self.title_color = title_color
        self.reading_input = False
        self.cursor = constants.CP437_CHAR_CURSOR_UNDERSCORE
        self.cursorposX = self.x + 2
        self.cursorposY = self.y + 6
        self.cursor_pos = 0
        self.inputposX = self.x + 2
        self.inputposY = self.y + 6
        self.messageposY = self.y +2

    def handle_input(self, key):
        if key.vk == tcod.KEY_CHAR:
            if key.shift:
                k = chr(key.c).capitalize()
            else:
                k = chr(key.c)

            self.input.insert(self.cursor_pos, k)
            self.cursor_pos += 1

            if len(self.input) <= self.viewport_max:
                self.viewport = list(self.input)
                self.cursorposX += 1
            else:
                self.viewport_end += 1
                self.viewport_start += 1
                self.viewport = self.input[self.viewport_start:self.viewport_end]

        elif key.vk == tcod.KEY_SPACE:
            self.input.insert(self.cursor_pos, " ")
            self.cursor_pos += 1

            if len(self.input) <= self.viewport_max:
                self.viewport = list(self.input)
                self.cursorposX += 1
            else:
                self.viewport_end += 1
                self.viewport_start += 1
                self.viewport = self.input[self.viewport_start:self.viewport_end]

        elif key.vk == tcod.KEY_LEFT and key.pressed:
            if self.cursorposX > self.x + 2:
                self.cursorposX -= 1
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
            if self.viewport_start > 0 and self.cursorposX == self.x + 2:
                self.viewport_start -= 1
                self.viewport_end -=1
                self.viewport = self.input[self.viewport_start:self.viewport_end]

        elif key.vk == tcod.KEY_RIGHT and key.pressed:
            if self.cursor_pos < len(self.input):
                self.cursor_pos += 1
                if self.cursorposX < self.w - 2:
                    self.cursorposX += 1

            if len(self.input) > self.viewport_max and len(self.input) > self.viewport_end and self.cursorposX == self.w - 2:
                self.viewport_end += 1
                self.viewport_start += 1
                self.viewport = self.input[self.viewport_start:self.viewport_end]

        elif key.vk == tcod.KEY_BACKSPACE:

            if self.cursor_pos > 0:
                del self.input[self.cursor_pos - 1]
                self.cursor_pos -= 1

            if self.cursorposX > self.x + 2 and len(self.input) <= self.viewport_max:
                self.cursorposX -= 1

            if self.viewport_start > 0 and self.viewport_end > self.viewport_max:
                self.viewport_start -= 1
                self.viewport_end -= 1
                if self.viewport_end < self.viewport_max:
                    self.viewport_end = self.viewport_max
                self.viewport = self.input[self.viewport_start:self.viewport_end]
            else:
                self.viewport = list(self.input)

        elif key.vk == tcod.KEY_ENTER and key.pressed:
            if self.reading_input:
                self.reading_input = False

    def draw_window(self):
        for i in range(self.x, self.w):
            for j in range(self.y, self.h):
                tcod.console_set_char_background(self.console, i, j, self.bg_color, tcod.BKGND_SET)
                tcod.console_put_char(self.console, i, j, " ")

        for i in range(self.x, self.w):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.y, tcod.CHAR_HLINE)

        for i in range(self.x, self.w):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.h, tcod.CHAR_HLINE)

        for i in range(self.y, self.h):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.x, i, tcod.CHAR_VLINE)

        for i in range(self.y, self.h):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.w, i, tcod.CHAR_VLINE)

        tcod.console_set_default_foreground(self.console, self.border_color)
        tcod.console_put_char(self.console, self.w, self.y, tcod.CHAR_NE)
        tcod.console_put_char(self.console, self.w, self.h, tcod.CHAR_SE)
        tcod.console_put_char(self.console, self.x, self.y, tcod.CHAR_NW)
        tcod.console_put_char(self.console, self.x, self.h, tcod.CHAR_SW)

        if self.message is not None:
            message_margin = len(self.message)
            mmarginX = ((self.w - self.x) - message_margin) / 2
            mmarginX = int(self.x + mmarginX)
            tcod.console_set_default_foreground(self.console, self.message_color)
            tcod.console_print(self.console, mmarginX, self.messageposY, self.message)

        if self.title is not None:
            title_margin = len(self.title)
            tmarginX = ((self.w - self.x) - title_margin) / 2
            tmarginX = int(self.x + tmarginX)
            tcod.console_set_default_foreground(self.console, self.title_color)
            tcod.console_print(self.console, tmarginX, self.y, self.title)

    def draw_cursor(self):
        t = time.time()
        t2 = int(t)
        t3 = t - t2
        if t3 > 0.5:
            tcod.console_set_default_foreground(self.console, self.cursor_color)
            tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, self.cursor)
        else:
            if len(self.viewport) > self.cursor_pos:
                tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, self.viewport[self.cursor_pos])
            else:
                tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, " ")

    def draw_input(self):
        ip = ""
        for i in self.viewport:
            ip += i
        tcod.console_print(self.console, self.inputposX, self.inputposY, ip)


class GameMenu(object):
    def __init__(self, console, state, x, border_color=Palette.WHITE.value, tab_color=Palette.GREEN.value,
                 message_color=Palette.WHITE.value):
        self.console = console
        self.state = state
        self.tab_color = tab_color
        self.message_color = message_color
        self.border_color = border_color
        self.x = x
        self.y = 0
        self.h = 50
        self.w = 20
        self.tabkey = ["1", "2", "3", "4", "5", "6"]
        self.selected_tab = 0
        self.wrapper = DocumentWrapper(width=self.w - 4)

    def _draw_tabs(self):
        tabpos = 2
        borderleft = 1
        borderright = 3
        for i in range(0, 6):
            if self.selected_tab == i:
                tcod.console_set_default_foreground(self.console, self.tab_color)
                tcod.console_put_char(self.console, self.x + tabpos, self.y, self.tabkey[i])
            else:
                tcod.console_set_default_foreground(self.console, self.border_color)
                tcod.console_put_char(self.console, self.x + tabpos, self.y, self.tabkey[i])

            tabpos += 3

        for i in range(0, 6):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.x + borderleft, self.y, constants.CP437_CHAR_TEEW)
            borderleft += 3

        for i in range(0, 6):
            tcod.console_set_char_foreground(self.console, self.x + borderright, self.y, self.border_color)
            tcod.console_put_char(self.console, self.x + borderright, self.y, constants.CP437_CHAR_TEEE)
            borderright += 3


    def _draw_border(self):
        for i in range(self.x, self.w + self.x):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.y, constants.CP437_CHAR_HLINE)

        for j in range(self.y, self.y + self.h):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.x, j, constants.CP437_CHAR_VLINE)

        tcod.console_set_default_foreground(self.console, self.border_color)
        tcod.console_put_char(self.console, self.x, self.y, constants.CP437_CHAR_NW)

    def _draw_class_description(self, message):
        tcod.console_set_default_foreground(self.console, self.message_color)
        ypos = 3
        tcod.console_print(self.console, self.x + 2, self.y + 2, "Description:")
        for line in message:
            tcod.console_print(self.console, self.x + 2, self.y + ypos, line)
            ypos += 1

        ypos += 4
        msg = self.wrapper.wrap("Press [esc] to go back.")
        for line in msg:
            tcod.console_print(self.console, self.x +2, self.y + ypos, line)
            ypos += 1

    def _draw_stats_selection(self, args):
        tcod.console_set_default_foreground(self.console, self.message_color)
        ypos = 3
        hint_pos = 0
        key_hint = ["a: ", "b: ", "c: ", "d: ", "e: ", "f: "]
        tcod.console_print(self.console, self.x + 2, self.y + 2, "Stat roll:")
        for arg in args:
            tcod.console_print(self.console, self.x + 2, self.y + ypos, key_hint[hint_pos] + str(arg))
            ypos += 1
            hint_pos += 1

        ypos += 4
        msg = self.wrapper.wrap("Press [a-f] to assign a stat.\n\nPress [enter] to continue.\n\nPress [esc] to go back.")
        for line in msg:
            tcod.console_print(self.console, self.x + 2, self.y + ypos, line)
            ypos += 1

    def draw_window(self, args=None):
        if self.state == "menu":
            self._draw_border()
            self._draw_tabs()

        if self.state == "class_description":
            self._draw_class_description(args["message"])

        if self.state == "stat_list":
            self._draw_stats_selection(args)


class StatSelect(object):
    def __init__(self, console, stats, x, y, w, h, title=None, selection_color=tcod.white, bg_color=tcod.black,
                 border_color=tcod.white, title_color=tcod.white, cursor_color=tcod.white):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.selecting = True
        self.backtrack = False
        self.selection_color = selection_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.title_color = title_color
        self.cursor_color = cursor_color
        self.stats = stats
        self.selection_count = len(self.stats)
        self.console = console
        self. defaults = [["strength ", -100], ["dexterity ", -100], ["constitution ", -100], ["intelligence ", -100], ["wisdom ", -100], ["charisma ", -100]]
        self.selections = [["strength ", -100], ["dexterity ", -100], ["constitution ", -100], ["intelligence ", -100], ["wisdom ", -100], ["charisma ", -100]]
        self.menu_select = 0
        self.cursorposX = self.x + 2
        self.cursorposY = self.y + 2

    def set_stats(self, stats):
        self.stats = stats
        self.selection_count = len(self.stats)

    def cursor_down(self):
        if self.menu_select < (self.selection_count - 1):
            self.menu_select += 1
            self.cursorposY += 2

    def cursor_up(self):
        if self.menu_select > 0:
            self.menu_select -= 1
            self.cursorposY -= 2

    def handle_input(self, key):
        if key.vk == tcod.KEY_ESCAPE:
            self.backtrack = True

        if key.vk == tcod.KEY_SPACE:
            self.selections[self.menu_select] = list(self.defaults[self.menu_select])

        elif key.vk == tcod.KEY_ENTER:
            full = [t[1] for t in self.selections]
            if sum(full) == 15:
                self.selecting = False

        elif key.vk == tcod.KEY_CHAR:
            revert = False
            if key.c == ord("a"):

                if self.selections[self.menu_select][1] == 0:
                    self.selections[self.menu_select][1] = -100
                    revert = True
                for i in self.selections:
                    if i[1] == 0:
                        i[1] = -100
                if not revert:
                    self.selections[self.menu_select][1] = 0

            elif key.c == ord("b"):
                if self.selections[self.menu_select][1] == 1:
                    self.selections[self.menu_select][1] = -100
                    revert = True
                for i in self.selections:
                    if i[1] == 1:
                        i[1] = -100
                if not revert:
                    self.selections[self.menu_select][1] = 1

            elif key.c == ord("c"):
                if self.selections[self.menu_select][1] == 2:
                    self.selections[self.menu_select][1] = -100
                    revert = True
                for i in self.selections:
                    if i[1] == 2:
                        i[1] = -100
                if not revert:
                    self.selections[self.menu_select][1] = 2

            elif key.c == ord("d"):
                if self.selections[self.menu_select][1] == 3:
                    self.selections[self.menu_select][1] = -100
                    revert = True
                for i in self.selections:
                    if i[1] == 3:
                        i[1] = -100
                if not revert:
                    self.selections[self.menu_select][1] = 3

            elif key.c == ord("e"):
                if self.selections[self.menu_select][1] == 4:
                    self.selections[self.menu_select][1] = -100
                    revert = True
                for i in self.selections:
                    if i[1] == 4:
                        i[1] = -100
                if not revert:
                    self.selections[self.menu_select][1] = 4

            elif key.c == ord("f"):
                if self.selections[self.menu_select][1] == 5:
                    self.selections[self.menu_select][1] = -100
                    revert = True
                for i in self.selections:
                    if i[1] == 5:
                        i[1] = -100
                if not revert:
                    self.selections[self.menu_select][1] = 5

    def draw_cursor(self):
        tcod.console_set_default_foreground(self.console, self.cursor_color)
        tcod.console_put_char(self.console, self.cursorposX, self.cursorposY, tcod.CHAR_ARROW2_E, tcod.BKGND_NONE)

    def draw_selections(self):
        tcod.console_set_default_foreground(self.console, self.selection_color)

        y = self.y + 2
        x = self.x + 4
        for selection in self.selections:
            s = ""
            if selection[1] == -100:
                s = selection[0] + "*)"
            else:
                selection_slot = ""
                if selection[1] == 0:
                    selection_slot = "a)"
                elif selection[1] == 1:
                    selection_slot = "b)"
                elif selection[1] == 2:
                    selection_slot = "c)"
                elif selection[1] == 3:
                    selection_slot = "d)"
                elif selection[1] == 4:
                    selection_slot = "e)"
                elif selection[1] == 5:
                    selection_slot = "f)"
                s = selection[0] + selection_slot + str(self.stats[selection[1]])

            tcod.console_print(self.console, x, y, s)
            y += 2

    def draw_window(self):
        for i in range(self.x, self.w):
            for j in range(self.y, self.h):
                tcod.console_set_char_background(self.console, i, j, self.bg_color, tcod.BKGND_SET)
                tcod.console_put_char(self.console, i, j, " ")

        for i in range(self.x, self.w):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.y, tcod.CHAR_HLINE)

        for i in range(self.x, self.w):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.h, tcod.CHAR_HLINE)

        for i in range(self.y, self.h):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.x, i, tcod.CHAR_VLINE)

        for i in range(self.y, self.h):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, self.w, i, tcod.CHAR_VLINE)

        tcod.console_set_default_foreground(self.console, self.border_color)
        tcod.console_put_char(self.console, self.w, self.y, tcod.CHAR_NE)
        tcod.console_put_char(self.console, self.w, self.h, tcod.CHAR_SE)
        tcod.console_put_char(self.console, self.x, self.y, tcod.CHAR_NW)
        tcod.console_put_char(self.console, self.x, self.h, tcod.CHAR_SW)

        title_margin = len(self.title)
        tmarginX = ((self.w - self.x) - title_margin) / 2
        tmarginX = int(self.x + tmarginX)
        marginY = int(((self.h - self.y) / 2) + self.y)
        if self.title is not None:
            tcod.console_set_default_foreground(self.console, self.title_color)
            tcod.console_print(self.console, tmarginX, self.y, self.title)


class MessageLog(object):
    def __init__(self, console, x, y, w, h, title, max_messages=50, messages_displayed=8, bg_color=tcod.black,
                 border_color=tcod.white, title_color=tcod.white):
        self.console = console
        self.max_messages = max_messages
        self.messages = []
        self.messages_displayed = messages_displayed
        self.message_start = 0
        self.message_end = 8
        self.message_cursor = 0
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.bg_color = bg_color
        self.border_color = border_color
        self.title_color = title_color

    def add_messages(self, messages):
        for message in messages:
            self.messages.append(message)
            self.message_cursor += 1
            if self.message_cursor > self.message_end:

                self.message_start += 1
                self.message_end +=1

        if self.message_end > self.max_messages:
            count = self.message_end - self.max_messages
            for i in range(count):
                self.message_cursor -= 1
                if self.message_cursor < self.message_start:
                    self.message_start -= 1
                    self.message_end -= 1


        self.messages = self.messages[:self.max_messages]
        self.message_end = len(self.messages)
        self.message_start = self.message_end - self.messages_displayed if self.message_end > self.messages_displayed else 0

    def draw_messages(self):
        ypos = self.y + 1
        l = self.messages_displayed if self.messages_displayed <= len(self.messages) else len(self.messages)
        for i in range(l):
            tcod.console_print(self.console, self.x, ypos, self.messages[self.message_start + i])
            ypos += 1

    def cursor_up(self):
        if self.message_start > 0:
            self.message_start -= 1
            self.message_end -= 1

    def cursor_down(self):
        if self.message_end < self.max_messages and self.message_end < len(self.messages):
            self.message_start += 1
            self.message_end += 1

    def draw_window(self):
        x2 = self.x + self.w
        y2 = self.y + self.h
        tx = self.x + 2
        arrowupY = self.y + 1
        arrowdownY = y2 - 1
        tcod.console_set_default_foreground(self.console, self.border_color)
        for i in range(self.x, x2):
            for j in range(self.y, y2):
                tcod.console_set_char_background(self.console, i, j, self.bg_color, tcod.BKGND_SET)
                tcod.console_put_char(self.console, i, j, " ")

        for i in range(self.x, x2):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, i, self.y, tcod.CHAR_HLINE)


        for i in range(self.y, y2):
            tcod.console_set_default_foreground(self.console, self.border_color)
            tcod.console_put_char(self.console, x2, i, tcod.CHAR_VLINE)

        tcod.console_put_char(self.console, x2, self.y, tcod.CHAR_NE)
        tcod.console_put_char(self.console, x2, arrowupY, tcod.CHAR_ARROW_N)
        tcod.console_put_char(self.console, x2, arrowdownY, tcod.CHAR_ARROW_S)
        tcod.console_set_default_foreground(self.console, self.title_color)
        tcod.console_print(self.console, tx, self.y, self.title)