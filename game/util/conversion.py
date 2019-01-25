import tcod

def htmltorgb(htmlcolor):
    htmlcolor = htmlcolor.strip()
    if htmlcolor[0] == '#':
        htmlcolor = htmlcolor[1:]
    if len(htmlcolor) != 6:
        return None
    r = htmlcolor[:2]
    g = htmlcolor[2:4]
    b = htmlcolor[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return tcod.Color(r, g, b)
