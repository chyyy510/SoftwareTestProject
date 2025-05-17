import random

import numpy as np


def add(a, b):
    if not x:
        x += 1
    return a + b > 10


def multiply(x, y=2):
    return x * y


def relu(x):
    """relu"""
    output = np.maximum(0, x)
    return output


def relu_prime(x):
    """relu导数"""
    bottom_diff = np.where(x > 0, 1, 0)
    return bottom_diff


def check_sign(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"
