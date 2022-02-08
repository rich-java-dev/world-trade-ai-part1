'''
Main entry point into program


World Trade/Transform Game Simulation


'''

# %%
import argparse
from node import Node


# %%
parser = argparse.ArgumentParser(
    description='CLI args to fine-tuning/running variants on the World Trade/Game Search')

parser.add_argument('--model', '--m', '-m',  default='',
                    type=str, help='Choosing Search function parameters')

parser.add_argument('--heuristic', '--htype', '-htype', default='',
                    type=str, help='Choosing Heuristic function model')

parser.add_argument('--depth',  '--d', '-d', default=10,
                    type=int, help='Search Depth of the model')

args = parser.parse_args()

model: str = args.model
heuristic: str = args.heuristic
depth: int = args.depth

# sanitize input here...
print(f'model:      {model}')
print(f'heuristic:  {heuristic}')
print(f'depth:      {depth}')


#
# initialize root node
#
root: Node = Node()

frontier = [root]  # search frontier - Implemented as a Priority Queue

# Collections of Nodes which represent viable solutions (depth achieved)
#  solutions contain the World State, history of transactions,
# and Utility function/measure of State quality at given step.
solutions = []


# Continue Search as long as there exists searchable nodes/expansion where depth has not been achieved
while(len(frontier) > 0):
    # Best First Search
    frontier.sort(key=lambda n: n.calc_quality(), reverse=True)
    node = frontier.pop(0)

    # check if bounded depth has been reached
    if(node.is_solution(depth)):
        print(f'Solution: {node.schedule}')
        print(f'quality: ' + str(node.calc_quality()))
        solutions.append(node)
        continue

    children = node.generate_successors()
    for child in children:
        frontier.append(child)

    # generate successors
