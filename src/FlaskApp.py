'''

World-Trade Scheduling AI - Agent

entry/driver or Front-End class for building
AI World Trading Schedules within the bounds/Rules of the
Simulation as Described.

author: Richard White

'''

# %%
import os
import copy
import pickle

from flask import Flask, request
from flask_cors import CORS

import policy
from node import Node
import visualize
import mathfunctions

from traverse import traverse_node


app = Flask(__name__)
CORS(app)


@app.route('/run', methods=['GET', 'POST'])
def run():

    depth: int = request.args.get('depth', default=3, type=int)
    soln_size: int = request.args.get('soln_set_size', default=5, type=int)
    initial_state_file: int = request.args.get(
        'initial_state_file', default=1, type=int)
    gamma: float = request.args.get('gamma', default=0.95, type=float)
    threshold: float = request.args.get('threshold', default=0.5, type=float)
    sched_threshold: float = request.args.get(
        'schedule_threshold', default=0.5, type=float)
    k: float = request.args.get('k', default=1., type=float)
    beam_width: int = request.args.get('beam_width', default=5250, type=int)
    max_checks: int = request.args.get('max_checks', default=10, type=int)

    output_dir = f'schedules/schedule-mstochastic-d{depth}-i{initial_state_file}-g{gamma}-k{k}-b{beam_width}-c{max_checks}-t{threshold}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    Node.gamma = gamma
    Node.threshold = threshold
    Node.sched_threshold = sched_threshold
    mathfunctions.k = k

    #
    # initialize root node
    #
    Node.init_state_idx = initial_state_file

    # Collections of Nodes which represent viable solutions (depth achieved)
    #  solutions contain the World State, history of transactions,
    # and Utility function/measure of State quality at given step.
    top_solutions = []
    min_eu = -1.

    policy.reload_policy()

    # instantiate a root node
    root: Node = Node()

    for i in range(max_checks):
        print(f"Iter: {i}")

        policy.reset_policy_checks()
        soln: Node = traverse_node(copy.deepcopy(root), depth)

        # don't bother putting in top solutions if cannot contend with the min expected utility already in the top_solutions
        if len(top_solutions) < soln_size or soln.calc_expected_utility() >= min_eu:

            top_solutions.append(soln)  # add solution to "top solutions"
            top_solutions.sort(key=lambda n: n.calc_expected_utility(),
                               reverse=True)  # sort top solutions
            while len(top_solutions) > soln_size:  # only keep the X best solutions
                removed_soln = top_solutions.pop()
            min_eu = min([soln.calc_expected_utility()
                          for soln in top_solutions])

    # Store Soltions in a 'pickled' list to learn from
    soln_pickle = "soln.pickle"
    with open(soln_pickle, 'wb') as outfile:
        pickle.dump(top_solutions, outfile)

    visualize.print_schedules(output_dir, top_solutions, max_checks)

    return {
        'text': visualize.get_schedules(top_solutions, max_checks),
        'image1': visualize.get_response_image(f'{output_dir}/schedule1.png'),
        'image2': visualize.get_response_image(f'{output_dir}/schedule2.png'),
        'image3': visualize.get_response_image(f'{output_dir}/schedule3.png'),
        'image4': visualize.get_response_image(f'{output_dir}/schedule4.png'),
        'image5': visualize.get_response_image(f'{output_dir}/schedule5.png')
    }


@app.route('/clear', methods=['POST'])
def clear():
    if os.path.exists("soln.pickle"):
        os.remove("soln.pickle")
    return ""


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
