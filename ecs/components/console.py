
class ConsoleHandler(object):
    def __init__(self, src_console, xsrc, ysrc, wsrc, hsrc, dst_console, xdst, ydst, fg_alpha=1.0, bg_alpha=1.0):
            self.src_console = src_console
            self.xsrc = xsrc
            self.ysrc = ysrc
            self.wsrc = wsrc
            self.hsrc = hsrc
            self.dst_console = dst_console
            self.xdst = xdst
            self.ydst = ydst
            self.fg_alpha = fg_alpha
            self.bg_alpha = bg_alpha