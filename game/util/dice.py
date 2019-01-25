import tcod


def roll(numdice, diesize, modifier=None, modifieramt=None, gaussian=None):
    generator = tcod.random_get_instance()
    if gaussian:
        tcod.random_set_distribution(generator, tcod.DISTRIBUTION_GAUSSIAN_RANGE)
    rolls = []
    for i in range(0, numdice):
        r = tcod.random_get_int(generator, 1, diesize)
        rolls.append(r)

    result = sum(rolls)
    if modifier is not None and modifieramt:
        if modifier == '+':
            result = result + modifieramt
        elif modifier == '-':
            result = result - modifieramt
        elif modifier == '*':
            result = result * modifieramt

    tcod.random_set_distribution(generator, tcod.DISTRIBUTION_LINEAR)
    return result


def d4(numdice=None, modifier=None, modifieramt=None, gaussian=None):
    if numdice is None:
        numdice = 1
    result = roll(numdice, 4, modifier=modifier, modifieramt=modifieramt, gaussian=gaussian)
    return result


def d6(numdice=None, modifier=None, modifieramt=None, gaussian=None):
    if numdice is None:
        numdice = 1
    result = roll(numdice, 6, modifier=modifier, modifieramt=modifieramt, gaussian=gaussian)
    return result


def d8(numdice=None, modifier=None, modifieramt=None, gaussian=None):
    if numdice is None:
        numdice = 1
    result = roll(numdice, 8, modifier=modifier, modifieramt=modifieramt, gaussian=gaussian)
    return result


def d10(numdice=None, modifier=None, modifieramt=None, gaussian=None):
    if numdice is None:
        numdice = 1
    result = roll(numdice, 10, modifier=modifier, modifieramt=modifieramt, gaussian=gaussian)
    return result


def d12(numdice=None, modifier=None, modifieramt=None, gaussian=None):
    if numdice is None:
        numdice = 1
    result = roll(numdice, 12, modifier=modifier, modifieramt=modifieramt, gaussian=gaussian)
    return result


def d20(numdice=None, modifier=None, modifieramt=None, gaussian=None):
    if numdice is None:
        numdice = 1
    result = roll(numdice, 20, modifier=modifier, modifieramt=modifieramt, gaussian=gaussian)
    return result


def d20advantage():
    r1 = d20()
    r2 = d20()
    return max(r1, r2)


def d20disadvantage():
    r1 = d20()
    r2 = d20()
    return min(r1, r2)