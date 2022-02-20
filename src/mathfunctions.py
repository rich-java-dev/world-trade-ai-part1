'''

Misc Math functions

'''

import numpy as np
import matplotlib.pyplot as plt

# basic sigmoid function implementation


def sigmoid(x) -> float:
    sig = np.where(x < 0, np.exp(x)/(1 + np.exp(x)), 1/(1 + np.exp(-x)))
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
