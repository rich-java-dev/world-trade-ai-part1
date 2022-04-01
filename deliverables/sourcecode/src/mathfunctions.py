'''

Misc Math functions

'''

import numpy as np
import matplotlib.pyplot as plt

# basic sigmoid function implementation

k = 1


def sigmoid(x, L=1, x_0=0) -> float:
    sig = L/(1 + np.exp(-k * (x-x_0)))
    return sig


# https://stats.stackexchange.com/questions/214877/is-there-a-formula-for-an-s-shaped-curve-with-domain-and-range-0-1
# this S/approximate Logistic curve is bounded to a domain of 0 to 1.
# This allows for custom stretching the domain, and scaling the range
# see also: https://en.wikipedia.org/wiki/Logit


def inv_logit_function(x, w=1, b=3) -> float:
    y: float = 1 / (1+(x/(w-x)) ** -b)
    return y


def inv_logit_decay_function(x, w=1, b=3) -> float:
    y: float = 1 / (1+(x/(w-x)) ** -b)
    return 1-y
