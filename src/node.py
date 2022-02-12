from dataclasses import dataclass, field
import copy
import pandas as pd
from resource import Resource
from country import Country
from world import WorldState
from events import Action, action_map

# define Node class so that can be referenced for redefining as Composite/Recursive manner


class Node():
    pass


'''
Search Node.

TreeNode-Like Structure, implementing an A* Search:

        A* :=  g + h,
        g := state quality function
        h := state heuristic function

        h necessarily never over-estimates (such that it is admissible).
        as Such, h derives its value by assuming a "minimal utilization"
        of a given resources 'potential'
'''

# opted against @dataclass, due to explicit lock-out of variable/"list" like mutable arrays
# @dataclass


class Node():

    # A dictionary of resources and properties.
    # These values placed on the objects could differ from others view on the material.
    resource_map: dict = {
        "R1": {},
        "R2": {},
        "R3": {}
    }

    # composite/tree pattern, can link back through parents to learn full path
    def __init__(self, parent: Node = None, action: str = "", state: WorldState = None):
        self.GAMMA: float = 0.64
        self.depth: int = 0  # the schedule/number of events triggered at given 'layer' in search
        self.action_map = action_map

        # describes the history which led to this specific node/state
        # NOTE: may replace with a function which builds the schedule by chaining together parent node calls
        self.schedule: list = []

        # transition states to scan next.
        self.children: list = []

        # deep copy required to prevent from modifying/passing around a single state object between depths
        self.state: WorldState = copy.deepcopy(state)
        if not state:
            self.state = WorldState()
            # self.state.countries[0].print()

        self.parent: Node = parent
        if parent:
            self.depth = parent.depth + 1
            self.schedule = [*parent.schedule, action]

        # apply action to parent Node to produce new State
        self.action: str = action

        if action in self.action_map and self.action_map[action].is_viable(self.state):
            self.action_map[action].apply(self.state)

    # The intrinsic quality of the State.

    def calc_quality(self):
        # assume we are first entry in a non-changing list of countries
        country = self.state.countries[0]

        q: float = 0

        for resource in country.resources.values():
            q = q + resource.quantity * resource.weight

        # define a utility function which calculates based on the current state.
        return q

    # A* search
    def calc_a_star(self, h=None) -> float:
        return self.calc_quality() + self.calc_heuristic()

    # defined as the "Net Gain" (or loss) from the Action which led to this Node.
    # N - (N - 1)
    def calc_reward(self) -> float:
        quality = self.calc_quality()
        prev_quality = quality
        if(self.parent):
            prev_quality = self.parent.calc_quality()
        return quality - prev_quality

    # defined as the 'net gain' discounted for having been on a schedule
    def calc_discounted_reward(self) -> float:
        return (self.GAMMA ** self.depth) * self.calc_reward()

    # for heuristic to be admissible, must never over-estimate quality
    def calc_heuristic(self, h=None) -> float:
        # define the heuristic
        return self.calc_discounted_reward()

    # check whether or not bounded/requested depth has been reached
    def is_solution(self, provided_depth) -> bool:
        # CHANGE: now searches to arbitrary depth, but doesn't demand depth to be reached to be viable solution
        # return True
        return provided_depth == self.depth

    '''
    Generate Successors
    Expands the current Node in all possible ways:
    All reachable states based on whether or not the Action provided is viable
    '''

    def generate_successors(self) -> list:
        children: list = []

        for action_id in self.action_map.keys():
            action: Action = self.action_map[action_id]
            # Check that action is allowed/viable given Action constraints
            if action.is_viable(self.state):
                child: Node = Node(self, action_id, self.state)
                children.append(child)

        self.children = children
        return children
