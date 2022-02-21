'''
Goals:

Heavily Integrated with State Quality.

Goals Define high level, "Declaritive" style parameters
Using Logistic functions to compute

'''

from abc import ABC, abstractmethod
from mathfunctions import sigmoid, inv_logit_function, inv_logit_decay_function
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
    def progress(self, state: WorldState, country_idx: int = 0) -> float:
        country = state.countries[country_idx]
        r1: Resource = country.resources['R1']  # analog to population
        r23: Resource = country.resources['R23']  # analog to housing

        if(r23.quantity == 0):
            return 0

        housing_ratio = r23.quantity/r1.quantity

        # Homelessenss quality following a Logistic Curve approximation mapped to domain 0-1
        # This w=0.8, and population starts at 100, with inverse logit creates range 0-80
        return r23.weight * r1.quantity * \
            (1 if housing_ratio >= 1 else
             inv_logit_function(housing_ratio))


class BalancedElectronics(Goal):
    # base calculation on number of electronics per house-hold. (NOT population)
    # There is also a max_cap of quality for Electronics per house-hold
    # This means exceeding this ratio does not improve quality

    def progress(self,  state: WorldState, country_idx: int = 0) -> float:
        country = state.countries[0]

        r1: Resource = country.resources['R1']  # analog to population
        r22: Resource = country.resources['R22']  # analog to electronics
        r23: Resource = country.resources['R23']  # analog to housing

        if(r23.quantity == 0):
            return 0
        if(r22.quantity == 0):
            return 0

        housing_ratio = r23.quantity/r1.quantity
        electronics_ratio = r22.quantity/r23.quantity
        max_cap = 2

        # Electronics quality following an Decaying inverse Logit Function:
        # in short, Electronics are a weighted sum, but also have a damping term applied relative to Housing sufficiency.
        # This encodes the idea that Houses/Housing Sufficiency impacts How useful electronics are at a given time:
        # If we have 100 electronics, and 1 house, this is out of balance.
        # However, if we have say, 50 houses, and up to around 50 electronics will have a fairly linear scaling, but beyond that, the
        # added benifit to more electronics have diminishing returns
        #
        # also dependent on housing ratio, such that electronics don't have as much impact until homelessness has mostly ended
        #
        return r22.weight * r22.quantity * housing_ratio * \
            (0 if electronics_ratio >= max_cap else
             inv_logit_decay_function(electronics_ratio, max_cap))


class MinimalWaste(Goal):
    # base calculation on number of electronics per house-hold. (NOT population)
    # There is also a max_cap of quality for Electronics per house-hold
    # This means exceeding this ratio does not improve quality

    def progress(self,  state: WorldState, country_idx: int = 0) -> float:
        country = state.countries[country_idx]

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
            housing_waste_ratio = r23p.quantity/(r23p.quantity + r23.quantity)

            waste += 0.1 * housing_waste_surplus * r23p.weight * \
                (1 if housing_waste_ratio == 1 else
                 inv_logit_function(housing_waste_ratio))

        # Apply similar thining to Electronics Waste
        elec_waste_surplus = r22p.quantity - r22.quantity
        if(elec_waste_surplus > 0):
            elec_waste_ratio = r22p.quantity / (r22.quantity + r22p.quantity)

            waste += 0.1 * elec_waste_surplus * r22p.weight * \
                (1 if elec_waste_ratio == 1 else
                 inv_logit_function(elec_waste_ratio))

        # Apply similar thinking to Alloy waste, however, we cap out with a ratio of  waste surplus to products produced
        alloy_waste_surplus = r21p.quantity - r21.quantity
        if(alloy_waste_surplus > 0):
            alloy_waste_ratio = r21p.quantity/(r21.quantity + r21p.quantity)

            waste += 0.1 * alloy_waste_surplus * r21p.weight * \
                (1 if alloy_waste_ratio == 1 else
                 inv_logit_function(alloy_waste_ratio))

        # waste is detrimental to quality calculation, so negate
        return -waste


class ResourcesOnHand(Goal):

    def progress(self,  state: WorldState, country_idx: int = 0) -> float:
        country = state.countries[country_idx]

        r1: Resource = country.resources['R1']  # analog to population
        r2: Resource = country.resources['R2']  # analog to metallic alloys
        r3: Resource = country.resources['R3']  # analog to metallic alloys
        r21: Resource = country.resources['R21']  # analog to metallic alloys
        r22: Resource = country.resources['R22']  # analog to electronics
        r23: Resource = country.resources['R23']  # analog to housing

        # simple weighted sum of resources per capita
        return (r21.quantity * r21.weight +
                r22.quantity * r22.weight +
                r2.quantity * (r2.weight + 0.05) +
                r3.quantity * (r3.weight + 0.05) +
                r23.quantity * r23.weight) /\
            r1.quantity


goal_map: dict = {
    'housing': EndHomelessness(),
    'electronics': BalancedElectronics(),
    'waste': MinimalWaste(),
    'raw_resources': ResourcesOnHand(),
}
