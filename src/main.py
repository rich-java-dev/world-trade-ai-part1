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

# %%
parser = argparse.ArgumentParser(
    description='CLI args to fine-tuning/running variants on the World Trade/Game Search')

parser.add_argument('--model', '--m', '-m',  default='DFS',
                    type=str, help='Choosing Search Model- \
                        DFS (greedy-local-depth-first-search \
                        UCS (uniform-cost search (Djikstra)')

# not applicable at moment
# parser.add_argument('--heuristic', '--htype', '-htype', default='',
#                     type=str, help='Choosing Heuristic function model')

parser.add_argument('--depth',  '--d', '-d', default=3,
                    type=int, help='Search Depth of the model')

parser.add_argument("--gamma", "--g", "-g", default=0.9,
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


parser.add_argument("--max_checks", "--c", "-c", default=10000,
                    type=int, help="set a fundamental cap on States checked in search. \
                        NOTE: node/state must not only be viable/non-zero probability, but must satisfy schedule needs")


# INPUT SANITATION:

args = parser.parse_args()
print(args)

model: str = args.model
# heuristic: str = args.heuristic
depth: int = args.depth
soln_size: int = args.soln_set_size
initial_state_file: int = args.initial_state_file
gamma: float = args.gamma
threshold: float = args.threshold
sched_threshold: float = args.schedule_threshold
k: float = args.k
beam_width: int = args.beam_width
max_checks: int = args.max_checks


output_dir = f'schedules/schedule-m{model}-d{depth}-i{initial_state_file}-g{gamma}-k{k}-b{beam_width}-c{max_checks}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


Node.gamma = gamma
Node.threshold = threshold
Node.sched_threshold = sched_threshold
mathfunctions.k = k

# supported models:
# UCS - Uniform Cost Search - uses Priority Queue/ Dijkstras search expanding/checking nodes with top cost regardless of depth
# DFS - Depth First Search - uses Priority Stack/expanding towards best quality function
if(model != "DFS"):
    model = "UCS"


#
# initialize root node
#
Node.init_state_idx = initial_state_file
root: Node = Node()


frontier = [root]  # search frontier

# Collections of Nodes which represent viable solutions (depth achieved)
#  solutions contain the World State, history of transactions,
# and Utility function/measure of State quality at given step.
top_solutions = []
soln_count: int = 0

min_eu = 0

# Continue Search as long as there exists searchable nodes/expansion where depth has not been achieved
while(len(frontier) > 0):

    # force out of search if max_checks are achieved. Could be a range of reasons
    # search needs to stopped prematurely after checks
    if soln_count >= max_checks:
        break

    # grab the last node in the list (treated as priority stack or queue)
    node = frontier.pop()

    # Avoid generating successors beyond this point
    # additional params to override and force a branch to be terminal/a leaf node
    # this indicates a terminal/invalid path: the leaf is not checked as a solution
    if node.force_leaf:
        continue

    # CLI/'TOP' like command, that refreshes/clears screen and reposts top solutions every 100 solns checked.
    soln_count += 1
    if(soln_count % 1000 == 0):
        visualize.print_top_solutions(top_solutions, soln_count)

    # keep a small list of top solutions, based on quality order
    soln = node  # copy.deepcopy(node)

    # don't bother putting in top solutions if cannot content with the min expected utility already in the top_solutions
    if soln.calc_expected_utility() > min_eu:

        top_solutions.append(soln)  # add solution to "top solutions"
        top_solutions.sort(key=lambda n: n.calc_expected_utility(),
                           reverse=True)  # sort top solutions
        while len(top_solutions) > soln_size:  # only keep the X best solutions
            removed_soln = top_solutions.pop()
        min_eu = min([soln.calc_expected_utility() for soln in top_solutions])

    # check if bounded depth has been reached - Recursive Base Case:
    # Avoid generating successors beyond this point
    if node.is_solution(depth):
        continue

    # if current depth is not a solution, then expand in all ways
    children = node.generate_successors()

    # append to list in reverse order for Depth (Priority Stack)
    # for Best First Search, sort Frontier, and not only successors
    if(model == "DFS"):
        children.sort(key=lambda n: n.calc_expected_utility())

    # Beam search: while still generating all successors, fine tune and only pursue those with highest quality
    while len(children) > beam_width:
        removed_soln = children.pop(0)

    # append successors to frontier
    frontier.extend(children)

    # Best First Search/Uniform Cost Search
    # for Depth First Search: comment this sort out,
    # and only sort successors prior to placing on frontier vs. sorting frontier
    # WARNING: this does impact the performance of the search
    if(model == "UCS"):
        frontier.sort(key=lambda n: n.calc_expected_utility())


visualize.print_schedules(output_dir, top_solutions, soln_count)
