
'''
 Policy

 This module aims to define a mechanism for the Search AI to construct a policy 
 from an optimal solution set, and implement as a solution in a Stochastic Model


'''


from abc import ABC, abstractmethod
import pickle

from world import WorldState
from node import Node
from country import Country
from resource import Resource
from events import Action, AlloyTemplate, HousingTemplate, ElectronicsTemplate


class Policy(ABC):

    @abstractmethod
    def actions(self) -> list:
        return [AlloyTemplate]

    @abstractmethod
    def conditions_met(self, world: WorldState) -> bool:
        return True


class TopSolutionPolicy(Policy):

    checked: bool = False

    def actions(self) -> list:
        actions = []

        try:
            with open('soln.pickle', 'rb') as infile:
                top_solutions = pickle.load(infile)
                actions = top_solutions[0].actions
        except Exception as ex:
            print("No pickled solution file found")

        return actions

    def conditions_met(self, world: WorldState) -> bool:
        if TopSolutionPolicy.checked:
            return False

        TopSolutionPolicy.checked = True
        try:
            with open('soln.pickle', 'rb') as infile:
                top_solutions = pickle.load(infile)
        except Exception as ex:
            print("No pickled solution file found")
            return False

        return True


class AlloyPolicy(Policy):

    def actions(self) -> list:
        return [AlloyTemplate]

    def conditions_met(self, world: WorldState) -> bool:
        return False


policies = {
    'top': TopSolutionPolicy(),
    'alloy': AlloyPolicy()
}


def meets_policy(world: WorldState) -> Policy:

    for k, policy in policies.items():
        if policy.conditions_met(world):
            return policy

    return


def apply_policy(node: Node, policy: Policy) -> Node:
    return node.apply(policy.actions())


def reset_policy_checks():
    TopSolutionPolicy.checked = False
