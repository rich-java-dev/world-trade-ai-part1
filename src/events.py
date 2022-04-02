'''
Events class definining all of the possible State transformations
which define the Edges in the Tree/Graph structure generated by step/time-evolving
the system.


name:       name/id of the transformation to be performed.
is_viable:  "SAT" problem (Is the input for the given Action/Transform "Satisfied"/viable

actions to be taken from the given

is_viable:  Checks whether the given state would permit such an action:
            ex: if required resources are met, action is viable
            If required resources are not met, action is not viable

apply:      "Pure" function taking in a given World State, and applies
            the underlying "Action" resulting in a new World State.

'''

from abc import ABC, abstractmethod
import copy

from world import WorldState
from country import Country
from resource import Resource
from mathfunctions import sigmoid
from quality import calc_quality

# Uses abstract methods as a means to express some static polymorphism/Inheritence


class Action(ABC):

    name: str

    @abstractmethod
    def is_viable(self, state: WorldState, **kwargs) -> bool:
        return False

    @abstractmethod
    def apply(self, state: WorldState, **kwargs):
        return 0

    @abstractmethod
    def probability(self, state: WorldState, **kwargs) -> float:
        return 1.0


class Transform(Action):

    def is_viable(self, state: WorldState, **kwargs) -> bool:
        return False

    # "Flux" like pattern, taking in a current state
    def apply(self, state: WorldState, **kwargs) -> int:
        return 0

    def probability(self, state: WorldState, **kwargs) -> float:
        return 1.0


'''
Alloys Template:
((TRANSFORM ?C (INPUTS (R1 1) (R2, 2)) (OUTPUTS (R1 1) (R21, 1) (R21’ 1)),
preconditions are of the form ?ARj <= ?C(?Rj)
'''


class AlloyTemplate(Transform):

    def is_viable(self, world: WorldState, **kwargs):
        c: Country = world.countries[0]
        return c.resources['R1'].quantity >= 1 \
            and c.resources['R2'].quantity >= 2

    # returns the 'factor' applied for the given base operation/inputs
    def apply(self, world: WorldState, **kwargs) -> int:
        c: Country = world.countries[0]

        # use about 2/3 of resources on given transform
        factor: int = max([1, int(c.resources['R2'].quantity / 3)])

        r2_consumed: int = factor * 2
        r21_gained: int = factor
        r21_waist_gained: int = factor

        c.resources['R2'].quantity -= r2_consumed
        c.resources['R21'].quantity += r21_gained
        c.resources["R21'"].quantity += r21_waist_gained

        return factor


'''
Electronics Template:
(TRANSFORM ?C (INPUTS (R1 3) (R2 2) (R21 2)) (OUTPUTS (R22 2) (R22’ 2) (R1 3)),
preconditions are of the form ?ARj <= ?C(?Rj)
'''


class ElectronicsTemplate(Transform):

    def is_viable(self, world: WorldState, **kwargs):
        c: Country = world.countries[0]
        return c.resources['R1'].quantity >= 3 \
            and c.resources['R2'].quantity >= 2 \
            and c.resources['R21'].quantity >= 2

    # returns the 'factor' applied for the given base operation/inputs
    def apply(self, world: WorldState, **kwargs) -> int:
        c: Country = world.countries[0]

        # use up to half of resources on given transform
        r2_max_factor: int = max([1, int(c.resources['R2'].quantity / 4)])
        r21_max_factor: int = max([1, int(c.resources['R21'].quantity / 4)])

        factor: int = min([r2_max_factor, r21_max_factor])

        r2_consumed: int = factor * 2
        r21_consumed: int = factor * 2

        r22_gained: int = factor * 2
        r22_waist_gained: int = factor * 2

        c.resources['R2'].quantity -= r2_consumed
        c.resources['R21'].quantity -= r21_consumed
        c.resources['R22'].quantity += r22_gained
        c.resources["R22'"].quantity += r22_waist_gained

        return factor


'''
Housing Template:
(TRANSFORM ?C (INPUTS (R1 5) (R2, 1) (R3 5) (R21 3) (OUTPUTS (R1 5) (R23, 1) (R23’ 1)),
preconditions are of the form ?AIk <= ?C(?Rk)
'''


class HousingTemplate(Transform):

    def is_viable(self, world: WorldState, **kwargs):
        c: Country = world.countries[0]
        return c.resources['R1'].quantity >= 5 \
            and c.resources['R2'].quantity >= 1 \
            and c.resources['R3'].quantity >= 5 \
            and c.resources['R21'].quantity >= 3

    # returns the 'factor' applied for the given base operation/inputs
    def apply(self, world: WorldState, **kwargs) -> int:
        c: Country = world.countries[0]

        # use up to half of resources on given transform
        r2_max_factor: int = max([1, int(c.resources['R2'].quantity)])
        r3_max_factor: int = max([1, int(c.resources['R3'].quantity / 5)])
        r21_max_factor: int = max([1, int(c.resources['R21'].quantity / 3)])

        factor: int = min([r2_max_factor, r3_max_factor, r21_max_factor])

        r2_consumed: int = factor
        r3_consumed: int = factor * 5
        r21_consumed: int = factor * 3

        r23_gained: int = factor
        r23_waist_gained: int = factor

        c.resources['R2'].quantity -= r2_consumed
        c.resources['R3'].quantity -= r3_consumed
        c.resources['R21'].quantity -= r21_consumed

        c.resources['R23'].quantity += r23_gained
        c.resources["R23'"].quantity += r23_waist_gained

        return factor


'''
Basic Transfer Template/Skeleton Implementation:
Potential Enhancements: Offer multi-Resource Trade Transactions:

{
    c1: 0, -- Country 1 in Trade Proposition
    c2: 1, -- Country 2 in Trade Proposition

    c1_offer: { -- Country 1 Trade Offer
        resource: 'R3'
        quantity: 100,
    },

    c2_offer: { -- Country 2 Trade Offer (Proposed By Country 1 Currently)
        resource: 'R21',
        quantity: 10,
    }
}

'''


class Transfer(Action):

    # Used to Prune searches which become 'untennable', based on some user-defined
    # threshold of probability of acceptance
    threshold = 0.5

    # Ensure Both Parties of required resources for said transfer
    def is_viable(self, world: WorldState, **kwargs) -> bool:

        c1_idx: int = kwargs['c1']
        c2_idx: int = kwargs['c2']

        c1: Country = world.countries[c1_idx]
        c1_offer: dict = kwargs['c1_offer']
        c1_offer_rsrc: str = c1_offer['resource']
        c1_offer_qty: int = int(c1_offer['quantity'])

        c2: Country = world.countries[c2_idx]
        c2_offer: dict = kwargs['c2_offer']
        c2_offer_rsrc: str = c2_offer['resource']
        c2_offer_qty: int = int(c2_offer['quantity'])

        # abort if trade resource requirements are infeasible
        if c1_offer_qty <= 0 or c2_offer_qty <= 0:
            return False

        # c1 cannot attempt to trade more than c1's resource quantity
        if c1_offer_qty > c1.resources[c1_offer_rsrc].quantity:
            return False

        # c2 cannot attempt to trade more than c1's resource quantity
        if c2_offer_qty > c2.resources[c2_offer_rsrc].quantity:
            return False

        # approximate a reasonable trade by assuming C1 cannot offer less than some threshold/ratio of C2s offer/value
        c1_est_value = c1_offer_qty * \
            (c1.resources[c1_offer_rsrc].weight + 0.1)
        c2_est_value = c1_offer_qty * \
            (c2.resources[c2_offer_rsrc].weight + 0.1)
        if c1_est_value / c2_est_value < Transfer.threshold:
            return False

        # return true if both Countries could 'feasibly' trade resource request
        return True

    def apply(self, world: WorldState, **kwargs) -> str:

        c1_idx: int = kwargs['c1']
        c2_idx: int = kwargs['c2']

        c1: Country = world.countries[c1_idx]
        c1_offer: dict = kwargs['c1_offer']
        c1_offer_rsrc = c1_offer['resource']
        c1_offer_qty = int(c1_offer['quantity'])

        c2: Country = world.countries[c2_idx]
        c2_offer: dict = kwargs['c2_offer']
        c2_offer_rsrc = c2_offer['resource']
        c2_offer_qty = int(c2_offer['quantity'])

        # Subtract resources from both countries, and then redistribute
        c1.resources[c1_offer_rsrc].quantity -= c1_offer_qty
        c2.resources[c2_offer_rsrc].quantity -= c2_offer_qty

        # reflect quantities:
        c1.resources[c2_offer_rsrc].quantity += c2_offer_qty
        c2.resources[c1_offer_rsrc].quantity += c1_offer_qty

        print_line = f'C{c1_idx+1}:{c1.name}  ({c1_offer_rsrc} x {c1_offer_qty}) to C{c2_idx+1}:{c2.name}  ({c2_offer_rsrc} x {c2_offer_qty})'

        return print_line

    def probability(self, world: WorldState, **kwargs) -> float:
        world_state: WorldState = copy.deepcopy(world)

        c1_offer: dict = kwargs['c1_offer']
        c1_offer_rsrc = c1_offer['resource']
        c1_offer_qty = int(c1_offer['quantity'])
        c1_idx: int = kwargs['c1']
        c2_idx: int = kwargs['c2']
        c2: Country = world_state.countries[c2_idx]

        c2_pre_qual: float = calc_quality(world_state, c2_idx)

        c2_offer: dict = kwargs['c2_offer']
        c2_offer_rsrc = c2_offer['resource']
        c2_offer_qty = int(c2_offer['quantity'])

        c2.resources[c2_offer_rsrc].quantity -= c2_offer_qty
        c2.resources[c1_offer_rsrc].quantity += c1_offer_qty

        c2_after_qual: float = calc_quality(world_state, c2_idx)
        c2_net_gain = c2_after_qual - c2_pre_qual

        # perform a sigmoid calculation based on the change in state quality if Country 2 Accepts Trade
        # any increases in state quality will
        sig = sigmoid(c2_net_gain)
        return sig


action_map: dict = {
    'Template - Alloy': AlloyTemplate(),
    'Template - Electronics': ElectronicsTemplate(),
    'Template - Housing': HousingTemplate(),
    'Transfer': Transfer(),
}
