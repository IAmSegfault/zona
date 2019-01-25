import random
import numpy as np
from math import log

def softmax(x):
    ex = np.exp(x - np.max(x))
    return ex / ex.sum()

def shannon_entropy(weights):
    x = log(sum(weights))
    z = []
    for i in weights:
        j = i * log(i)
        z.append(j)
    y = sum(z) / sum(weights)
    return x - y

#Turns a set of weights into probabilites and returns a choice
def weighted_choice(choices):
    if type(choices) == dict:
        total = sum(w for c, w in choices.items())
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices.items():
            if upto + w >= r:
                return c
            upto += w

    elif type(choices) == list:
        total = sum(i for i in choices)
        r = random.uniform(0, total)
        upto = 0
        for i in range(0, len(choices)):
            if upto + choices[i] >= r:
                return i
            upto += choices[i]


def string_to_int32(s):
    x = int.from_bytes(s.encode(), 'little')
    x -= 2147483647
    return x % (2**32 - 1)


def neighbors(matrix, radius, rowNumber, columnNumber):
    m = [[matrix[i][j] if  i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0]) else None
            for j in range(columnNumber-1-radius, columnNumber+radius)]
            for i in range(rowNumber-1-radius, rowNumber+radius)]
    return np.array(m)