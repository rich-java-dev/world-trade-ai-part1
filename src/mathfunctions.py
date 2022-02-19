'''

Misc Math functions

'''

import numpy as np
import matplotlib.pyplot as plt

# basic sigmoid function implementation


def sigmoid(x) -> float:
    sig = np.where(x < 0, np.exp(x)/(1 + np.exp(x)), 1/(1 + np.exp(-x)))
    return sig


def test_plot():
    rng = np.linspace(-10, 10, 20, endpoint=False)
    plt.plot([x for x in rng],
             [sigmoid(x) for x in rng])
    plt.show()

# https://stats.stackexchange.com/questions/214877/is-there-a-formula-for-an-s-shaped-curve-with-domain-and-range-0-1
# this S/approximate Logistic curve is bounded to a domain of 0 to 1.
# This allows for custom stretching the domain, and scaling the range
# see also: https://en.wikipedia.org/wiki/Logit


def inv_logit_function(x, w=1, b=3) -> float:
    y: float = 1 / (1+(x/(w-x)) ** -b)
    return y


def test_plot():

    w: float = 3
    rng = np.linspace(0, w, 100, endpoint=False)
    plt.plot([x for x in rng],
             [inv_logit_function(x, w) for x in rng])
    plt.show()
