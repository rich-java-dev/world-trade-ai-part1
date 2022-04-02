from dataclasses import dataclass, field
import copy
import math
from resource import Resource
from country import Country
from world import WorldState
from events import Action, action_map
from quality import calc_quality

# define Node class so that can be referenced for redefining as Composite/Recursive manner


class Node():
    pass


'''
Search Node data structure.

Can be implemented in Main class as either a Uniform Cost/Best First Search,
or a Greedy/Local Depth First (default)

Uses a composite like pattern, and tracks the "world state".
Each node is a representation of the world state after N events have occured (given depth of search)

children: the successors of the cur rent world state
schedule: list of events/actions which led to this state
schedule_probablity: likelihood an event

'''

# opted against @dataclass, due to explicit lock-out of variable/"list" like mutable arrays
# @dataclass


class Node():

    id: int = -1  # visited node number. incremented as class variable
    init_state_idx: int = 1  # default file enum. 1,2,3,4 supported
    gamma: float = 0.64  # decay function, for discounting rewards
    # acceptible schedule success probability, used for pruning based on definable threshold
    sched_threshold = 0.50
    threshold = 0.50

    # composite/tree pattern, can link back through parents to learn full path
    def __init__(self, parent: Node = None, state: WorldState = None, action: str = "", **kwargs):

        # flag used to indicate an abrupt override/pruning of a branch and force the current node to become a leaf node.
        self.force_leaf = False
        # id, which will aim to represent the ID/occurance/step' in the State Search from the inital start point
        Node.id += 1
        self.id = Node.id

        self.depth: int = 0  # the schedule/number of events triggered at given 'layer' in search
        self.action_map = action_map

        # describes the history which led to this specific node/state
        # NOTE: may replace with a function which builds the schedule by chaining together parent node calls
        self.schedule: list = []
        self.schedule_probability: list = [1.0, ]
        # Expected Utility is the sum of incremental increases at each step determined by the discounted reward
        self.expected_utility: list = [0., ]

        self.likelihood = 1.0  # probability of the current specific action succeeding

        # transition states to scan next.
        self.children: list = []

        # deep copy required to prevent from modifying/passing around a single state object between depths
        self.state: WorldState = copy.deepcopy(state)
        if not state:
            self.state = WorldState(Node.init_state_idx)
            # self.state.countries[0].print()

        #
        self.parent: Node = parent
        if parent:
            self.depth = parent.depth + 1
            self.schedule = [*parent.schedule, action]
            self.schedule_probability = [*parent.schedule_probability, ]
            self.expected_utility = [*parent.expected_utility, ]

        # apply action to parent Node to produce new State
        self.action: str = action
        if action in self.action_map and \
                self.action_map[action].is_viable(self.state, **kwargs):

            # track likelihood/probability of Trade being accepted by other Country
            self.likelihood = self.action_map[action].probability(
                self.state, **kwargs)

            self.schedule_probability.append(self.likelihood)

            if self.likelihood < Node.threshold or \
                    self.calc_schedule_probability() < Node.sched_threshold:
                self.force_leaf = True

            factor = self.action_map[action].apply(self.state, **kwargs)

            self.expected_utility.append(self.calc_discounted_reward())
            # TODO - procress kwargs into action
            # factor is the applied number of units of the underlying transform
            self.schedule[-1] += f' x {factor} \t Q:{round(self.calc_quality(), 3)} \t EU:{round(self.calc_expected_utility(),3)}'

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

    # defined as the 'net gain' discounted for having been on a schedule, and further discounted by probability of (acceptance/likelihood)
    def calc_discounted_reward(self) -> float:
        return (Node.gamma ** self.depth) * self.calc_reward() * self.likelihood

    def calc_heuristic(self, h=None) -> float:
        # define the heuristic
        return self.calc_discounted_reward()

    # check whether or not bounded/requested depth has been reached
    def is_solution(self, provided_depth) -> bool:
        # CHANGE: now searches to arbitrary depth, but doesn't demand depth to be reached to be viable solution
        # return True
        return provided_depth == self.depth

    def calc_schedule_probability(self) -> float:
        return math.prod(self.schedule_probability)

    def calc_expected_utility(self) -> float:
        return sum(self.expected_utility)
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

    '''
    Generate Successors for Transfers:
    The general approach taken is:
    1) Create a 'template'/'contract', which involves 2 parties, and 2 resources (and quantities of the resource)
    2) Iterate over tradable resources, and vary by percentage of Country 1's resources an amount to offer
    3) Ensure both parties have required resources to perform trade (Don't allow debt/negative quantities)
    4) Subtract Trade Resource from both Countries
    5) Add Trade Resource/Qty from other party from
    6) Yield the new Node which results from the completed trade
    7) When the new node is instantiated, the probability and impact of the trade are expanded/applied
    '''

    def generate_transfer_successors(self):
        world = self.state
        action_id: str = 'Transfer'
        action: Action = action_map[action_id]

        # "R21'", "R22'", "R23'"]
        resource_list: list = ["R2", "R3",
                               "R21", "R22", "R21'", "R22'", "R23'"]
        percent_interval: list = [1.00, .75, .5, .25, .10]
        # Building a Schedule for Country '0' - Atlantis
        c1_idx = 0
        c1 = world.countries[c1_idx]

        # 5- for loop structure using list comprehensions
        # max fan out/complexity:
        # (7 resources from C1)(6 resources from C2)(5 countries other than C1)(5 quantity steps over C1 resource)(5 quantity steps over C2 resource)
        # = (7)(6)(5)(5)(5) = 5,250 : however not all of these states are reachable so don't become successors.
        # for example, at beginning of run, no countries have wastes, and most only have 2 resources, so most 1st moves approx: (2)(1)(5)(5)(5) = 250
        return [n for n in (self.collect_children_nodes(c1_idx, c2_idx, r1_offer, r1_qty, r2_offer, r2_qty)
                            for r1_offer in resource_list

                            for r2_offer in resource_list if r2_offer is not r1_offer

                            for r1_qty in (int(r1_pct * c1.resources[r1_offer].quantity)
                                           for r1_pct in percent_interval) if r1_qty != 0

                            for c2_idx in range(len(world.countries)) if c2_idx is not c1_idx

                            for r2_qty in (int(r2_pct * self.state.countries[c2_idx].resources[r2_offer].quantity)
                                           for r2_pct in percent_interval) if r2_qty != 0

                            ) if n is not None]

    def collect_children_nodes(self, c1_idx, c2_idx, r1_offer, r1_qty, r2_offer, r2_qty):

        # Adhere to API/expectation defined in EVENTS/TRANSFER class
        proposition: dict = {
            'c1': c1_idx,
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

        # confirm both countries have the required resources in above proposition to proceed.
        # additionally confirm the schedule is still 'viable', and falls within some definable probability bounds
        if action_map['Transfer'].is_viable(self.state, **proposition):

            child: Node = Node(
                self, self.state, 'Transfer', **proposition)
            return child

    '''
    Convenience method for printing out the Schedule of the Node/WorldState
    '''

    def get_schedule(self) -> str:
        result: str = ''
        for i in range(len(self.schedule)):
            entry = self.schedule[i]
            ln = f'{i+1}: {entry}\n'
            result += ln
        result += f'Schedule Probability: {self.schedule_probability} = {self.calc_schedule_probability()}\n'
        result += f'id: {self.id}\n'
        return result
