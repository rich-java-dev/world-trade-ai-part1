from dataclasses import dataclass, field
import copy
import pandas as pd
from resource import Resource
from country import Country
from world import WorldState


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

    state: WorldState  # the world/global state at a particular Node

    depth: int = 0  # the schedule/number of events triggered at given 'layer' in search

    # describes the history which led to this specific node/state
    # NOTE: may replace with a function which builds the schedule by chaining together parent node calls
    schedule: list = []

    # action which led to this node
    action: str = ""

    # parent node
    parent: Node

    # transition states to scan next.
    children: list = []

    # set of allowable actions, defining events which trigger state transition
    actions: list = ['A', 'B', 'C']

    def action_a(self) -> WorldState:
        c: Country = self.state.countries[0]
        r: Resource = c.resources[0]
        r.quantity = r.quantity + 100

    def action_b(self):
        c: Country = self.state.countries[0]
        r: Resource = c.resources[0]
        r.quantity = r.quantity - 100

    def action_c(self):
        c: Country = self.state.countries[0]
        r: Resource = c.resources[0]
        r.quantity = r.quantity + 50

    action_map: dict = {
        'A': action_a,
        'B': action_b,
        'C': action_c
    }

    # A dictionary of resources and properties.
    # These values placed on the objects could differ from others view on the material.
    resource_map: dict = {
        "R1": {},
        "R2": {},
        "R3": {}
    }

    # composite/tree pattern, can link back through parents to learn full path
    def __init__(self, parent: Node = None, action: str = "", state: WorldState = None):

        self.state = copy.deepcopy(state)
        if not state:
            self.state = WorldState()
            self.state.countries[0].print()

        self.state.countries = copy.deepcopy(self.state.countries)

        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
            self.schedule = [*parent.schedule, action]

        # apply action to parent Node to produce new State
        self.action = action

        if action in self.action_map:
            self.action_map[action](self)

    # The intrinsic quality of the State.

    def calc_quality(self):
        # assume we are first entry in a non-changing list of countries
        country = self.state.countries[0]

        q: float = 0

        for resource in country.resources:
            q = q + resource.quantity * resource.weight

        # define a utility function which calculates based on the current state.
        return q

    # for heuristic to be admissible, must never over-estimate quality
    def calc_heuristic(self, h=None) -> float:
        # define the heuristic
        if not h:
            return 0

        return h

    # A* search
    def calc_a_star(self, h=None) -> float:
        return self.calc_quality() + self.calc_heuristic()

    # defined as the "Net Gain" (or loss) from the Action which led to this Node.
    # N - (N - 1)
    def calc_reward(self) -> float:
        return self.calc_quality() - self.parent.calc_quality()

    # defined as the 'net gain' discounted for having been on a schedule
    def calc_discounted_reward(self) -> float:
        return 0.9 * self.calc_reward()

    # check whether or not bounded/requested depth has been reached
    def is_solution(self, provided_depth) -> bool:
        return provided_depth == self.depth

    '''
    Generate Successors
    Expands the current Node in all possible ways:
    All reachable states based on whether or not the Action provided is viable
    '''

    def generate_successors(self) -> list:
        children: list = []

        for action in self.actions:

            child: Node = Node(self, action, self.state)

            children.append(child)

        self.children = children
        return children
