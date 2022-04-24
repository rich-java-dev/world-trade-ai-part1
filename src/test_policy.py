from policy import policies
from node import Node


node: Node = Node()


policy = policies['top']

if policy.conditions_met(node.state):
    node = node.apply(policy.actions())

print(node.get_schedule())
