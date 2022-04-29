import os
import matplotlib.pyplot as plt

import io
from base64 import encodebytes
from PIL import Image

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
            soln = top_solutions[i]

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


def get_schedule_str(node: Node) -> str:

    sched: str = node.get_schedule()
    q = round(node.calc_quality())
    eu = round(node.calc_expected_utility())
    return f' \
    \nSchedule: \
    \n{sched} \
    \nstate quality : {q} \
    \nexpected utility: {eu} \
    \n'


def get_schedules(top_solutions: list, soln_count) -> str:
    # Search finished: print the top results

    schedules = '\n\n'.join([get_schedule_str(n) for n in top_solutions])

    return f' \
    \n\
    \nTop Solutions: \
    \n\
    \nTotal Nodes generated: {Node.id} \
    \n\
    \nTotal Plausible Schedules checked: {soln_count} \
    \n\
    \n{schedules} \
    \n\
    '


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


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img
