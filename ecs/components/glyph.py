import tcod

class Glyph(object):
    def __init__(self, character, color_fg, color_bg=None):
        self.character = character
        self.color_fg = color_fg
        self.color_bg = color_bg

class FOWGlyph(Glyph):
    def __init__(self, character, color_fg, color_bg=None):
        super().__init__(character, color_fg, color_bg)
        self.visited = False
        self.in_view = False
        fg_r = color_fg.r
        fg_r = max(0, fg_r - 63)

        fg_g = color_fg.g
        fg_g = max(0, fg_g - 63)

        fg_b = color_fg.b
        fg_b = max(0, fg_b - 63)

        self.color_fg_oov = tcod.Color(fg_r, fg_g, fg_b)
        if self.color_bg is not None:
            bg_r = color_bg.r
            bg_r = max(0, bg_r - 63)

            bg_g = color_bg.g
            bg_g = max(0, bg_g - 63)

            bg_b = color_bg.b
            bg_b = max(0, bg_b - 63)
            self.color_bg_oov = tcod.Color(bg_r, bg_g, bg_b)
        else:
            self.color_bg_oov = None