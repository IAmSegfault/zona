import tcod

def wander(**kwargs):
    goal = kwargs["goal"]
    brain = kwargs["brain"]
    gwk = kwargs["gwk"]

    rng = tcod.random_get_instance()
    r = tcod.random_get_int(rng, 0, 7)
    direction = None
    if r == 0:
        direction = "east"
    elif r == 1:
        direction = "west"
    elif r == 2:
        direction = "north"
    elif r == 3:
        direction = "south"
    elif r == 4:
        direction = "northwest"
    elif r == 5:
        direction = "northeast"
    elif r == 6:
        direction = "southwest"
    elif r == 7:
        direction = "southeast"

    gwk.syscall("mob_move_local", direction=direction)
    goal.finished = True
