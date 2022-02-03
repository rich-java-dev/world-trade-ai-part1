'''
Main entry point into program

'''
# %%
import argparse
import pandas as pd
from models import WorldState, Country, Resource

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

frontier = [] # search
solutions = [] # Nodes which represent viable solutions (depth achieved)



def transform(transform: str) -> None:
    transform_map[transform]
    transform.apply(world_state)


while(curr_depth < depth):
    break
