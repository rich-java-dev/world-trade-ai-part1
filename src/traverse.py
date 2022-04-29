'''

World-Trade Scheduling AI - Agent

entry/driver or Front-End class for building
AI World Trading Schedules within the bounds/Rules of the
Simulation as Described.

author: Richard White

'''

# %%
import os
import argparse
import random
import copy
import math
import pickle

import policy
from node import Node
import visualize
import mathfunctions

'''
Define a Markov Decision Process Traversal of the Node,
either applying applicable Policies or
performaning Stocastic Search Behavior weighted by (discounted) Expected Utility

'''


def traverse_node(node: Node, depth: int) -> Node:
    if node.is_solution(depth):
        return node

    # Implement Policy Check
    policy_present = policy.meets_policy(node.state)

    if policy_present and random.random() > 0.5:
        successor = policy.apply_policy(node, policy_present, depth)
        return traverse_node(successor, depth)

    else:  # No Policy found, so use Stochastic/weighted search
        children = [n for n in node.generate_successors()
                    if not n.force_leaf]
        children.sort(key=lambda n: n.calc_expected_utility())

        # use expected utility to weight the decision tree, but use EU in terms of
        weights = [n.calc_expected_utility() for n in children]

        # calc min weight to use as a shift constant towards a small number
        try:
            min_weight = abs(min(weights))
            weights = [w+min_weight for w in weights]
            if sum(weights) == 0:
                weights = [1. for w in weights]

        except Exception as e:
            print(e)
            return node

        # weighted pseudo-random selection from possible successors
        successor: Node = random.choices(
            children, [math.exp(w) for w in weights], k=1)[0]

        return traverse_node(successor, depth)
