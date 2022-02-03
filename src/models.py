from dataclasses import dataclass


@dataclass
class WorldState:
    counties: list = []


@dataclass
class Country:
    name: str = ""
    resources: list = []


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


@dataclass
class Node:

    state: WorldState  # the world/global state at a particular Node

    depth: int = 0  # the schedule/number of events triggered at given 'layer' in search
    quality: float = 0  # the aggregation of state quality at this node/state

    schedule: list = []  # describes the history which led to this specific node/state
    children: list = []  # transition states to scan next.
