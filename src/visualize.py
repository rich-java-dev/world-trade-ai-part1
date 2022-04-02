import os
import matplotlib.pyplot as plt
from node import Node

'''
Visualizations tools for plotting Histograms/State evolutions/tracking over time

'''


def print_schedules(output_dir: str, top_solutions: list, soln_count: int):
    # Search finished: print the top results
    print("Top Solutions: ")
    with open(f'{output_dir}/schedules.txt', 'a+') as output:
        print('')
        print(f'Total Nodes generated: {Node.id}')
        print(f'Total Plausible Schedules checked: {soln_count}')
        output.write('Top Solutions:\n')
        soln = None

        for i in range(len(top_solutions)):
            soln = top_solutions.pop(0)

            for prt in [output.write, print]:
                soln.state.countries[0].printer = prt
                prt('Schedule:\n')
                prt(soln.get_schedule())
                prt(f'quality: {round(soln.calc_quality())}\n')
                prt(f'expected utility: {round(soln.calc_expected_utility())}')
                prt(f'State:\n')
                soln.state.countries[0].print()
                prt(f'\n')
                plot_and_save(soln, f'{output_dir}-{i+1}',
                              f"{output_dir}/schedule{i+1}.png")


def print_top_solutions(top_solutions: list, soln_count):
    '''
    Render a human readable statistics of the on-going search in progress, including the 'top' results

    '''
    # windows vs. linux variant
    os.system('cls')  # os.system('clear')

    print(f'States found: {soln_count}')

    for soln in top_solutions:
        print(f'Schedule: ')
        print(soln.get_schedule())
        print(f'quality: {round(soln.calc_quality(), 3)}')
        print(f'expected utility: {round(soln.calc_expected_utility())}')
        print(f'State:')
        soln.state.countries[0].print()
        print('')


def plot_and_save(node: Node, title: str, output_file: str):
    max_depth = node.depth

    fig, axs = plt.subplots(1, max_depth+1, sharex=True, sharey=True)
    fig.suptitle(f"{title}\nC1:\n{node.get_schedule()}", x=0, ha='left')

    for i in range(max_depth+1):

        resources: list = node.state.countries[0].resources

        keys = resources.keys()
        vals = [r.quantity for r in resources.values()]

        axes = axs if max_depth == 0 else axs[max_depth - i]

        axes.bar(keys, vals)
        axes.set_title(
            f'{max_depth - i} \n \
                Q={round(node.calc_quality(), 3)} \n \
                EU={round(node.calc_expected_utility(), 3)}')
        axes.set_ylabel("Qty")
        node = node.parent

    # plt.tight_layout()
    plt.subplots_adjust(top=0.5)

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(output_file)
