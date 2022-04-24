'''

World-Trade Scheduling AI - Agent

entry/driver or Front-End class for building
AI World Trading Schedules within the bounds/Rules of the
Simulation as Described.

author: Richard White

'''

# %%
import os
import argparse
from node import Node
import visualize
import mathfunctions
import random
import copy
import policy
import math


# %%
parser = argparse.ArgumentParser(
    description='CLI args to fine-tuning/running variants on the World Trade/Game Search')

# not applicable at moment
# parser.add_argument('--heuristic', '--htype', '-htype', default='',
#                     type=str, help='Choosing Heuristic function model')

parser.add_argument('--depth',  '--d', '-d', default=3,
                    type=int, help='Search Depth of the model')

parser.add_argument("--gamma", "--g", "-g", default=0.95,
                    type=float, help='Decay constant gamma, \
                        which dampens/discounts the quality function: domain [0-1]')

parser.add_argument("--k", "-k", default=2.,
                    type=float, help='Logistic Curve Steepness constant')

parser.add_argument("--threshold", "--t", "-t", default=0.50, type=float,
                    help='Probability Threshold: Do not pursue schedules \
                        which are less likely than desired likelihood: domain [0-1]')

parser.add_argument("--schedule_threshold", "--st", "-st", default=0.50, type=float,
                    help='Probability Threshold: Do not pursue schedules \
                        which are less likely than desired likelihood: domain [0-1]')

parser.add_argument('--soln_set_size',  '--s', '-s', default=5,
                    type=int, help='Number of Solutions (Depth achieved) to track in the best solutions object')

parser.add_argument('--initial_state_file',  '--i', '-i', default=1,
                    type=int, help='enum 1-4. initial state file for loading the simulation/search: \
                        1) resource rich country in world with uneven resource distribution (NORMAL MODE) \
                        2) resource poor country in world with uneven resource distribution (BRUTAL MODE) \
                        3) resource moderate country in world with even resource distribution (EASY MODE) \
                        4) resource poor country in world with even resource distribution (HARD MODE) \
                        ')

parser.add_argument("--beam_width", "--b", "-b", default=5250,
                    type=int, help="used to prune/reduce search size by limiting \
                        the maximum number of successor nodes placed on the stack at each step")


parser.add_argument("--max_solutions", "--c", "-c", default=100,
                    type=int, help="set a fundamental cap on how many satisfiable schedules searched. \
                        NOTE: node/state must not only be viable/non-zero probability, but must satisfy schedule needs")


# INPUT SANITATION:

args = parser.parse_args()
print(args)

# heuristic: str = args.heuristic
depth: int = args.depth
soln_size: int = args.soln_set_size
initial_state_file: int = args.initial_state_file
gamma: float = args.gamma
threshold: float = args.threshold
sched_threshold: float = args.schedule_threshold
k: float = args.k
beam_width: int = args.beam_width
max_checks: int = args.max_solutions


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

# Define a non-back tracking, stochastic (probabilistic) 'walk' until depth bound is reached.


def traverse_node(node: Node, depth: int) -> Node:
    if node.is_solution(depth):
        return node

    # Implement Policy Check
    policy_present = policy.meets_policy(node.state)
    if policy_present:
        successor = policy.apply_policy(node, policy_present)
        return traverse_node(successor, depth)

    else:  # No Policy found, so use Stochastic/weighted search
        children = [n for n in node.generate_successors() if not n.force_leaf]
        children.sort(key=lambda n: n.calc_expected_utility())

        # use expected utility to weight the decision tree, but use EU in terms of
        weights = [n.calc_expected_utility() for n in children]

        # calc min weight to use as a shift constant towards a small number
        try:
            min_weight = abs(min(weights))
            weights = [w+min_weight for w in weights]
            if sum(weights) == 0:
                weights = [1 for w in weights]
        except Exception as e:
            print(e)
            return node

        # weighted pseudo-random selection from possible successors
        successor: Node = random.choices(
            children, [math.exp(w) for w in weights], k=1)[0]

        return traverse_node(successor, depth)


# Collections of Nodes which represent viable solutions (depth achieved)
#  solutions contain the World State, history of transactions,
# and Utility function/measure of State quality at given step.
top_solutions = []
soln_count: int = 0

min_eu = -1.

# instantiate a root node
root: Node = Node()

for i in range(max_checks):
    print(f"Iter: {i}")

    policy.reset_policy_checks()
    soln: Node = traverse_node(copy.deepcopy(root), depth)

    # don't bother putting in top solutions if cannot content with the min expected utility already in the top_solutions
    if len(top_solutions) < soln_size or soln.calc_expected_utility() >= min_eu:

        top_solutions.append(soln)  # add solution to "top solutions"
        top_solutions.sort(key=lambda n: n.calc_expected_utility(),
                           reverse=True)  # sort top solutions
        while len(top_solutions) > soln_size:  # only keep the X best solutions
            removed_soln = top_solutions.pop()
        min_eu = min([soln.calc_expected_utility() for soln in top_solutions])


visualize.print_schedules(output_dir, top_solutions, max_checks)
