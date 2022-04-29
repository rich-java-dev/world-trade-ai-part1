import numpy as np
import matplotlib.pyplot as plt

from mathfunctions import inv_logit_function, inv_logit_decay_function, sigmoid


def test_sigmoid_plot():
    rng = np.linspace(-10, 10, 100, endpoint=False)
    plt.plot([x for x in rng],
             [sigmoid(x) for x in rng])
    plt.show()


def test_inv_logit_plot():

    w: float = 1
    rng = np.linspace(0, w, 100, endpoint=False)
    plt.plot([x for x in rng],
             [inv_logit_function(x, w) for x in rng])
    plt.show()


def test_inv_logit_decay_plot():
    w: float = 3
    rng = np.linspace(0, w, 100, endpoint=False)
    plt.plot([x for x in rng],
             [inv_logit_decay_function(x, w) for x in rng])
    plt.show()


test_sigmoid_plot()
# test_inv_logit_plot()
# test_inv_logit_decay_plot()
