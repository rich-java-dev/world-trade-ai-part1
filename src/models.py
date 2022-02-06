from dataclasses import dataclass
'''
World State Object
'''


@dataclass
class WorldState:
    counties: list = []

    # load in world state
    def init(self):
        return


'''
Country structure:

County Name/Identifier, and Material listing of each countries resources

'''


@dataclass
class Country:
    name: str = ""
    resources: list = []


'''
Resources structure:

The fundamental 'material' commodities which Countries aim to use to optimize their Goals/agenda/state quality.

Resources have the following properties:

construction/infrastructure:
energy:
technology/R&D:
nutrition:
liquidity:
culture:

'''


@dataclass
class Resource:

    resource_id: int = 0
    quantity: int = 0
    name: str = ""
    descript: str = ""
    critical_resource: bool = False

    price: float = 0

    def heuristic_value(self) -> float:
        return self.unit_price * self.quantity_on_hand

    def calc_utility_to_cost_ratio(self, utility_function) -> float:
        utility_function(self)


class Node:

    state: WorldState  # the world/global state at a particular Node

    depth: int = 0  # the schedule/number of events triggered at given 'layer' in search
    quality: float = 0  # the aggregation of state quality at this node/state

    schedule: list = []  # describes the history which led to this specific node/state

    # action which led to this node
    action: str = ""
    parent: Node
    children: list = []  # transition states to scan next.

    # set of allowable actions, defining events which trigger state transition
    actions: list = []

    # composite/tree pattern, can link back through parents to learn full path
    def __init__(self, parent: Node, action: str):
        self.parent = parent
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

            children.insert(child)

        self.children = children
        return children
