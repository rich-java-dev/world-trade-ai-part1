from world import WorldState
from resource import Resource
from goals import goal_map


'''
State Quality Function - 

This state quality function has changed over time, 
but generally aims to represent the Relative 'Rating' of a given society.

In the real world, this could pertain to a sum or weight of ratings across different domains such as
infrastructure, water quality, air quality, socio-economic values, intra-country resource distribution, etc.

'''


def calc_quality(state: WorldState) -> float:

    housing_goal = goal_map['housing'].progress(state)
    electronics_goal = goal_map['electronics'].progress(state)
    waste_goal = goal_map['waste'].progress(state)
    resource_on_hand_goal = goal_map['raw_resources'].progress(state)

    q = housing_goal+electronics_goal+waste_goal+resource_on_hand_goal
    return q
