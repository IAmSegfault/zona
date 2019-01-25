'''
A python port of https://github.com/IAmSegfault/N3N
Useful for example, when creating a deterministic seed for a given chunk coordinate.
(x,y,z)->(x combine 1)+((x+y+1) combine 2)+((x+y+z+2) combine 3).
See https://math.stackexchange.com/questions/1176184/how-to-find-unique-numbers-from-3-numbers
https://math.stackexchange.com/questions/312879/how-to-define-a-injective-and-surjective-function-from-mathbbz-to-mathbb
https://en.wikipedia.org/wiki/Combination#Example_of_counting_combinations
for details.
'''
maxint = 262144
maxmagic = 68719476735
maxint32 = 1024
maxmagic32 = 4194303
magic = 9001

def constraint(j):
    if j > 0:
        j = 2 * j
    else:
        j = (-2 * j) + 1

    return j

def constraint_unsigned32(j):
    j -= 1
    if j > 0:
        j = 2 * j
    else:
        j = (-2 * j) + 1

    return j

def combine(n, k):
    c = 1
    for i in range(1, k + 1):
        x = n - (i - 1)
        c = (x / i) * c

    return c


def injection_map(x, y, z=0, w=False):
    x = constraint(x)
    y = constraint(y)
    z = constraint(z)

    n1 = x
    x1 = combine(n1, 1)

    n2 = x + y + 1
    x2 = combine(n2, 2)

    n3 = x + y + z + 2
    x3 = combine(n3, 3)

    r = x1 + x2 + x3

    if r > maxint:
        return None

    if w and abs(w) <= maxmagic:
        r = r * w
    else:
        r = r * magic

    r = r + 0.5 - (r + 0.5) % 1

    return r

# From 0-15
def injection_map32(x, y, z, w=False):
    x = constraint_unsigned32(x)
    y = constraint_unsigned32(y)
    z = constraint_unsigned32(z)

    n1 = x
    x1 = combine(n1, 1)

    n2 = x + y + 1
    x2 = combine(n2, 2)

    n3 = x + y + z + 2
    x3 = combine(n3, 3)

    r = x1 + x2 + x3

    if r > maxint32:
        return None

    if w and abs(w) <= maxmagic32:
        r = r * w
    else:
        r = r * magic

    r = r + 0.5 - (r + 0.5) % 1

    return r


def tetrahedral(x, y, z):
    ny = x + y
    ny = ny * 0.5 * (ny + 1)
    nz = x + y + z
    mod3 = nz % 3
    if mod3 == 1:
        nz = (nz + 2) / 6 * nz * (nz + 1)
    elif mod3 == 2:
        nz = (nz + 1) / 6 * nz * (nz + 2)
    else:
        nz = nz / 6 * (nz + 1) * (nz + 2)

    return x + ny + nz


def zn(z):
    return z < 0 and 1 - 2 * z or 2 * z


def biject(x ,y, z):
    return tetrahedral(zn(x), zn(y), zn(z))


def bijection_map32(x, y, z=0, w=127, map_bits=24):
    bijection = biject(x,y,z)
    maxmagic = int(((2**32) - 1) / 2**map_bits)
    if w > maxmagic or bijection > 2**map_bits:
        return None
    else:
        return bijection * w