import matplotlib.pyplot as plt
from node import Node


def plot(node: Node):
    max_depth = node.depth

    fig, axs = plt.subplots(1, max_depth+1, sharex=True, sharey=True)
    fig.suptitle(node.print_schedule(), x=0.1, ha='left')

    c_idx = 0

    for i in range(max_depth+1):

        resources: list = node.state.countries[0].resources

        keys = resources.keys()
        vals = [r.quantity for r in resources.values()]

        axes = axs if max_depth == 0 else axs[max_depth - i]

        axes.bar(keys, vals)
        axes.set_title(
            f'C{c_idx+1} - at depth: {max_depth - i}, quality={node.calc_quality()}')
        axes.set_ylabel("Qty")
        node = node.parent

    plt.tight_layout()
    plt.show()
