import numpy as np
import random


def add(a, b):
    return a + b


def multiply(x, y=2):
    return x * y

def relu(x):
  ''' relu '''
  output=np.maximum(0,x)
  return output

def relu_prime(x):
    ''' relu导数 '''
    bottom_diff=np.where(x > 0, 1, 0)
    return bottom_diff


