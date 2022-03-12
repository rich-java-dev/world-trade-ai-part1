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

parser.add_argument('--depth',  '--d', '-d', default=5,
                    type=int, help='Search Depth of the model')

parser.add_argument('--soln_set_size',  '--s', '-s', default=2,
                    type=int, help='Number of Solutions (Depth achieved) to track in the best solutions object')

parser.add_argument('--initial_state_file',  '--i', '-i', default=1,
                    type=int, help='enum 1-4. initial state file for loading the simulation/search')

parser.add_argument('--output', '--o', '-o', default='schedule.txt',
                    type=str, help='The output file to print the top Schedules to')


args = parser.parse_args()

model: str = args.model
# heuristic: str = args.heuristic
depth: int = args.depth
soln_size: int = args.soln_set_size
output_file: str = args.output
initial_state_file: int = args.initial_state_file


# sanitize input here...

# supported models:
# UCS - Uniform Cost Search - uses Priority Queue/ Dijkstras search expanding/checking nodes with top cost regardless of depth
# DFS - Depth First Search - uses Priority Stack/expanding towards best quality function
if(model != "DFS"):
    model = "UCS"

print(f'model:      {model}')
# print(f'heuristic:  {heuristic}')
print(f'depth:      {depth}')
print()

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


def print_top_solutions():
    '''
    Render a human readable statistics of the on-going search in progress, including the 'top' results

    '''
    # windows vs. linux variant
    os.system('cls')  # os.system('clear')

    print(f'States found: {soln_count}')

    for soln in top_solutions:
        print(f'Schedule: ')
        soln.print_schedule()
        print(f'quality: {soln.calc_quality()}')
        print(f'State:')
        soln.state.countries[0].print()
        print('')
        print('')

    # Continue Search as long as there exists searchable nodes/expansion where depth has not been achieved
while(len(frontier) > 0):

    # grab the 0th node on the Stack (or Queue)
    node = frontier.pop()

    # keep a small list of top solutions, based on quality order
    soln = node  # copy.deepcopy(node)

    top_solutions.append(soln)  # add solution to "top solutions"
    top_solutions.sort(key=lambda n: n.calc_quality(),
                       reverse=True)  # sort top solutions
    while len(top_solutions) > soln_size:  # only keep the X best solutions
        removed_soln = top_solutions.pop()

    # CLI/'TOP' like command, that refreshes/clears screen and reposts top solutions every 100 solns checked.
    soln_count += 1
    if(soln_count % 500 == 0):
        print_top_solutions()

    # check if bounded depth has been reached - Recursive Base Case:
    # Avoid generating successors beyond this point
    if(node.is_solution(depth)):
        # print(f'Solution: {node.schedule}')
        # print(f'quality: ' + str(node.calc_quality()))
        # print(f'State:')
        # node.state.countries[0].print()
        # print()
        continue

    # if current depth is not a solution, then expand in all ways
    children = node.generate_successors()

    # append to list in reverse order for Depth (Priority Stack)
    # for Best First Search, sort Frontier, and not only successors
    if(model == "DFS"):
        children.sort(key=lambda n: n.calc_discounted_reward())

    # append successors to frontier at 'beginning' of list
    for child in children:
        frontier.append(child)

    # Best First Search/Uniform Cost Search
    # for Depth First Search: comment this sort out,
    # and only sort successors prior to placing on frontier vs. sorting frontier
    # WARNING: this does impact the performance of the search
    if(model == "UCS"):
        frontier.sort(key=lambda n: n.calc_discounted_reward())


# Search finished: print the top results
print("Top Solutions: ")
with open(output_file, 'a+') as output:
    print('')
    print(f'Total States Found: {soln_count}')
    output.write('Top Solutions:\n')
    while(len(top_solutions) > 0):
        soln = top_solutions.pop(0)

        for prt in [output.write]:
            soln.state.countries[0].printer = prt
            prt('Schedule:\n')
            prt(soln.print_schedule())
            prt(f'quality: {soln.calc_quality()}\n')
            prt(f'State:\n')
            soln.state.countries[0].print()
            prt(f'\n')
