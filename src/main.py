'''
Main entry point into program

'''
# %%
import argparse
from models import Node

#
#  Look-ahead
#
# %%
parser = argparse.ArgumentParser(
    description='CLI args to fine-tune/run various ')
parser.add_argument('--model', '--m', '-m',  default='',
                    type=str, help='Choosing Heuristic/Utility function parameters')
parser.add_argument('--depth',  '--d', '-d', default=10,
                    type=int, help='Search Depth of the model')
args = parser.parse_args()

model: str = args.model
depth: int = args.depth

# sanitize input here...

print(f'Model: {model}')
print(f'Depth: {depth}')

# initialize root node
root: Node = Node()

frontier = [root]  # search frontier
solutions = []  # Nodes which represent viable solutions (depth achieved)


def calc_quality():
    return


while(len(frontier) > 0):
    node = frontier.pop(0)

    # check if bounded depth has been reached
    if(node.is_solution(depth)):
        print(f'Solution: {node.schedule}')
        solutions.append(node)
        continue

    children = node.generate_successors()
    for child in children:
        frontier.append(child)

    # generate successors
