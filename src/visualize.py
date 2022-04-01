import matplotlib.pyplot as plt
from node import Node

'''
Visualizations tools for plotting Histograms/State evolutions/tracking over time

'''


def plot(node: Node):
    max_depth = node.depth

    fig, axs = plt.subplots(1, max_depth+1, sharex=True, sharey=True)
    fig.suptitle("C1:\n" + node.print_schedule(), x=0, ha='left')

    for i in range(max_depth+1):

        resources: list = node.state.countries[0].resources

        keys = resources.keys()
        vals = [r.quantity for r in resources.values()]

        axes = axs if max_depth == 0 else axs[max_depth - i]

        axes.bar(keys, vals)
        axes.set_title(
            f'{max_depth - i}\nQ={round(node.calc_quality(), 3)}\nDU={round(node.calc_discounted_reward(), 3)}')
        axes.set_ylabel("Qty")
        node = node.parent

    # plt.tight_layout()
    plt.subplots_adjust(top=0.5)
    plt.show()
