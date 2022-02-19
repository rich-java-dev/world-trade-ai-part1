'''
Main entry point into program

World Trade/Transform Game Simulation

'''

# %%
import argparse
from node import Node
import copy

# %%
parser = argparse.ArgumentParser(
    description='CLI args to fine-tuning/running variants on the World Trade/Game Search')

parser.add_argument('--model', '--m', '-m',  default='UCS',
                    type=str, help='Choosing Search Model')

parser.add_argument('--heuristic', '--htype', '-htype', default='',
                    type=str, help='Choosing Heuristic function model')

parser.add_argument('--depth',  '--d', '-d', default=5,
                    type=int, help='Search Depth of the model')

parser.add_argument('--soln_set_size',  '--s', '-s', default=10,
                    type=int, help='Number of Solutions (Depth achieved) to track in the best solutions object')

parser.add_argument('--output', '--o', '-o', default='schedule.txt',
                    type=str, help='The output file to print the top Schedules to')


args = parser.parse_args()

model: str = args.model
heuristic: str = args.heuristic
depth: int = args.depth
soln_size: int = args.soln_set_size
output_file: str = args.output


# sanitize input here...

# supported models:
# UCS - Uniform Cost Search - uses Priority Queue/ Dijkstras search expanding/checking nodes with top cost regardless of depth
# DFS - Depth First Search - uses Priority Stack/expanding towards best quality function
if(model != "UCS"):
    model = "DFS"

print(f'model:      {model}')
print(f'heuristic:  {heuristic}')
print(f'depth:      {depth}')
print()

#
# initialize root node
#
root: Node = Node()

frontier = [root]  # search frontier

# Collections of Nodes which represent viable solutions (depth achieved)
#  solutions contain the World State, history of transactions,
# and Utility function/measure of State quality at given step.
top_solutions = []

# Continue Search as long as there exists searchable nodes/expansion where depth has not been achieved
while(len(frontier) > 0):

    # Best First Search/Uniform Cost Search
    # for Depth First Search: comment this sort out,
    # and only sort successors prior to placing successors on frontier
    if(model == "UCS"):
        frontier.sort(key=lambda n: n.calc_discounted_reward(), reverse=True)

    # grab the 0th node on the Stack (or Queue)
    node = frontier.pop(0)

    # check if bounded depth has been reached - Recursive Base Case
    if(node.is_solution(depth)):
        print(f'Solution: {node.schedule}')
        print(f'quality: ' + str(node.calc_quality()))
        print(f'State:')
        node.state.countries[0].print()
        print()
        continue

    # keep a small list of top solutions, based on quality order
    soln = copy.deepcopy(node)
    top_solutions.append(soln)  # add solution to "top solutions"
    top_solutions.sort(key=lambda n: n.calc_quality(),
                       reverse=True)  # sort top solutions
    while len(top_solutions) > soln_size:  # only keep the X best solutions
        removed_soln = top_solutions.pop()

    # if current depth is not a solution, then expand in all ways
    children = node.generate_successors()

    # append to list in reverse order for Depth (Priority Stack)
    # for Best First Search, sort Frontier, and not only successors
    if(model == "DFS"):
        children.sort(key=lambda n: n.calc_discounted_reward(), reverse=True)

    # append successors to frontier
    for child in children:
        frontier.append(child)


# Search finished: print the top results
print("Top Solutions: ")
with open(output_file, 'a+') as output:
    output.write('Top Solutions:\n')

    while(len(top_solutions) > 0):
        soln = top_solutions.pop(0)

        for prt in [print, output.write]:
            soln.state.countries[0].printer = prt
            prt(f'Solution: {soln.schedule}\n')
            prt(f'quality: {soln.calc_quality()}\n')
            prt(f'State:\n')
            soln.state.countries[0].print()
            prt(f'\n')
