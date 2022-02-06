'''
Main entry point into program

'''
# %%
import argparse
import pandas as pd
from models import WorldState, Country, Resource, Node

#
#  PRICER - Produces Stock price data onto a given Kafka server
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

print(model)
print(depth)

world_state = WorldState()
curr_depth = 0


# initialize root node
root: Node = Node()

frontier = [root]  # search
solutions = []  # Nodes which represent viable solutions (depth achieved)


def calc_quality():
    return


while(len(frontier) > 0):
    node = frontier[0]

    #check if bounded depth has been reached
    if(node.is_solution(depth)):
        solutions.append(node)
        continue

    children = node.generate_successors()

    # generate successors 
    frontier.append(children)
