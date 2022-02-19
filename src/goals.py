'''
Goals:

Heavily Integrated with State Quality.

Goals Define high level, "Declaritive" style parameters
Using Logistic functions to compute

'''

from abc import ABC, abstractmethod
from mathfunctions import sigmoid, inv_logit_function
from world import WorldState
from resource import Resource


'''
     A Goal class which defines a single method, "Progress" towards completing the goal.

'''


class Goal(ABC):

    @abstractmethod
    def progress(self, state: WorldState) -> float:
        return 0


# country = state.countries[0]
# r1: Resource = country.resources['R1']  # analog to population
# # penalize unspect quantity on hand.
# r2: Resource = country.resources['R2']  # analog to metallic elements
# r3: Resource = country.resources['R3']  # analog to timber

# r21: Resource = country.resources['R21']  # analog to metallic alloys
# r22: Resource = country.resources['R22']  # analog to electronics
# r23: Resource = country.resources['R23']  # analog to housing

# r21p: Resource = country.resources["R21'"]  # metallic waste
# r22p: Resource = country.resources["R22'"]  # electronics waste
# r23p: Resource = country.resources["R23'"]  # housing waste

class EndHomelessness(Goal):

    # base calculation on a ratio of percentage of unhoused people, presuming 1:1 population to housing unit
    def progress(self, state: WorldState) -> float:
        country = state.countries[0]
        r1: Resource = country.resources['R1']  # analog to population
        r23: Resource = country.resources['R23']  # analog to housing

        if(r23.quantity == 0):
            return 0

        housing_ratio = r23.quantity/r1.quantity
        if(housing_ratio >= 1):
            return r1.quantity

        # Homelessenss quality following a Logistic Curve approximation mapped to domain 0-1
        return r1.quantity * inv_logit_function(housing_ratio)


class BalancedElectronics(Goal):
    # base calculation on number of electronics per house-hold. (NOT population)
    # There is also a max_cap of quality for Electronics per house-hold
    # This means exceeding this ratio does not improve quality

    def progress(self,  state: WorldState) -> float:
        country = state.countries[0]
        r23: Resource = country.resources['R23']  # analog to housing
        r22: Resource = country.resources['R22']  # analog to electronics

        if(r23.quantity == 0):
            return 0
        if(r22.quantity == 0):
            return 0

        electronics_ratio = r22.quantity/r23.quantity
        max_cap = 5
        if(electronics_ratio >= max_cap):
            return r23.quantity

        # Electronics quality following a Logistic Curve approximation mapped to domain 0-1
        return r23.quantity * inv_logit_function(electronics_ratio, 5)


class MinimalWaste(Goal):
    # base calculation on number of electronics per house-hold. (NOT population)
    # There is also a max_cap of quality for Electronics per house-hold
    # This means exceeding this ratio does not improve quality

    def progress(self,  state: WorldState) -> float:
        country = state.countries[0]

        r21: Resource = country.resources['R21']  # analog to metallic alloys
        r22: Resource = country.resources['R22']  # analog to electronics
        r23: Resource = country.resources['R23']  # analog to housing

        r21p: Resource = country.resources["R21'"]  # metallic waste
        r22p: Resource = country.resources["R22'"]  # electronics waste
        r23p: Resource = country.resources["R23'"]  # housing waste

        waste = 0

        # There is Threshold/"Tolerance" for Waste Up to some threshold of relation to the underlying resource causing the waste.
        # Once exceeded, the detrimental impact on quality kicks in:
        # eg: If I have 100 Housing Units, and 100 Housing Waste, thats considered acceptable,
        # however, if I have 100 Housing Units, and 200 Housing waste, that far exceeds the expectation, and causes a rectifying term to kick in

        housing_waste_surplus = r23p.quantity - r23.quantity
        if(housing_waste_surplus > 0):
            housing_waste_ratio = r23p.quantity/(r23.quantity + r23p.quantity)

            waste += housing_waste_surplus * \
                inv_logit_function(housing_waste_ratio) /\
                (r21.quantity + r22.quantity + r23.quantity)

        # Apply similar thining to Electronics Waste
        elec_waste_surplus = r22p.quantity - r22.quantity
        if(elec_waste_surplus > 0):
            elec_waste_ratio = r22p.quantity / (r22.quantity + r22p.quantity)

            waste += elec_waste_surplus * \
                inv_logit_function(elec_waste_ratio) /\
                (r21.quantity + r22.quantity + r23.quantity)

        # Apply similar thinking to Alloy waste, however, we cap out with a ratio of  waste surplus to products produced
        alloy_waste_surplus = r21p.quantity - r21.quantity
        if(alloy_waste_surplus > 0):
            alloy_waste_ratio = r21p.quantity/(r21.quantity + r21p.quantity)

            waste += alloy_waste_surplus * \
                inv_logit_function(alloy_waste_ratio) /\
                (r21.quantity + r22.quantity + r23.quantity)

        # waste is detrimental to quality calculation, so negate
        return -waste


class ResourcesOnHand(Goal):

    def progress(self,  state: WorldState) -> float:
        return 0


goal_map: dict = {
    'housing': EndHomelessness(),
    'electronics': BalancedElectronics(),
    'waste': MinimalWaste(),
    'raw_resources': ResourcesOnHand(),
}
