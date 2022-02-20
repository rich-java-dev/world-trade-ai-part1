from dataclasses import dataclass, field
import copy
from resource import Resource
from country import Country
from world import WorldState
from events import Action, action_map
from quality import calc_quality

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

    # composite/tree pattern, can link back through parents to learn full path
    def __init__(self, parent: Node = None, state: WorldState = None, action: str = "", **kwargs):
        self.GAMMA: float = 0.80
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

        if action in self.action_map and self.action_map[action].is_viable(self.state, **kwargs):

            factor = self.action_map[action].apply(self.state, **kwargs)
            # TODO - procress kwargs into action
            # factor is the applied number of units of the underlying transform
            self.schedule[-1] += f' x {factor}'

    # The intrinsic quality of the State.

    def calc_quality(self):
        return calc_quality(self.state)

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

            if(action_id == 'Transfer'):
                children.extend(self.generate_transfer_successors())
                continue

            # Check that action is allowed/viable given Action constraints
            if action.is_viable(self.state):
                child: Node = Node(self, self.state, action_id)
                children.append(child)

        self.children = children
        return children

    def generate_transfer_successors(self) -> list:
        world = self.state
        successors: list = []
        action_id: str = 'Transfer'
        action: Action = action_map[action_id]

        resource_list: list = ['R2', 'R3', 'R21', 'R22']

        c1 = world.countries[0]
        for r1_offer in resource_list:
            r1: Resource = c1.resources[r1_offer]
            if r1.quantity == 0:
                continue

            for c2_idx in range(1, len(world.countries)):
                c2: Country = world.countries[c2_idx]  # 2nd country in trade

                for r2_offer in resource_list:
                    r2: Resource = c2.resources[r2_offer]
                    if r2.quantity == 0:
                        continue
                    if r1.name == r2.name:
                        continue

                    for percentage in [0.10, 0.25, 0.35, 0.50]:

                        r1_qty = int(percentage * r1.quantity)
                        r2_qty = int(percentage * r1.quantity)

                        proposition: dict = {
                            'c1': 0,
                            'c2': c2_idx,
                            'c1_offer': {
                                'resource': r1_offer,
                                'quantity': r1_qty,
                            },
                            'c2_offer': {
                                'resource': r2_offer,
                                'quantity': r2_qty,
                            },
                        }

                        if action.is_viable(world, **proposition):
                            child: Node = Node(
                                self, world, action_id, **proposition)

                            successors.append(child)

        return successors

    def print_schedule(self):

        for i in range(len(self.schedule)):
            entry = self.schedule[i]
            print(f'{i+1}: {entry}')
