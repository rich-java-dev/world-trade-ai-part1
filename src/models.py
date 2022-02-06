from dataclasses import dataclass, field
import pandas as pd

'''
World State Object
'''


class WorldState:
    counties: list = []

    # load in world state
    def init(self):
        return


'''
Country structure:

County Name/Identifier, and Material listing of each countries resources

'''


class Country:
    name: str = ""
    resources: list = []


'''
Resources structure:

The fundamental 'material' commodities which Countries aim to use to optimize their Goals/agenda/state quality.

Resources have the following properties:

utility:
construction/infrastructure:
energy:
technology/R&D:
nutrition:
liquidity:
culture:

Resources also have a function which gives an aggregate admissible heuristic 
(metric based on its "least useful" attribute based on how a resource gets utiltized in the least useful way)
This is also akin to a Mini-Max search, in which the "opponent" is minimizing the value I can get out of a resource.

'''


class Resource:

    resource_id: int = 0
    name: str = ""

    quantity: int = 0

    utility: int = 0
    construction: int = 0
    energy: int = 0
    technology: int = 0
    nutrition: int = 0
    liquidity: int = 0
    culture: int = 0

    descript: str = ""
    critical_resource: bool = False

    price: int = 0

    def heuristic_value(self) -> float:
        return self.unit_price * self.quantity_on_hand

    def calc_utility_to_cost_ratio(self, utility_function) -> float:
        utility_function(self)


class Node:
    pass


class Node:

    state: WorldState  # the world/global state at a particular Node

    depth: int = 0  # the schedule/number of events triggered at given 'layer' in search
    quality: float = 0  # the aggregation of state quality at this node/state

    # describes the history which led to this specific node/state
    schedule: list = []

    # action which led to this node
    action: str = ""
    parent: Node

    # transition states to scan next.
    children: list = []

    # set of allowable actions, defining events which trigger state transition
    actions: list = ['A', 'B', 'C']

    # composite/tree pattern, can link back through parents to learn full path
    def __init__(self, parent: Node = None, action: str = ""):
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
            self.schedule = [*parent.schedule, action]
        self.action = action

        # apply action to parent Node to produce new State

    # check whether or not bounded/requested depth has been reached

    def calc_utility(self):
        # define a utility function which calculates based on the current state.
        return 0

    def is_solution(self, provided_depth) -> bool:
        return provided_depth == self.depth

    def generate_successors(self) -> list:
        children: list = []

        for action in self.actions:

            child: Node = Node(self, action)

            children.append(child)

        self.children = children
        return children
