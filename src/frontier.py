'''

Frontier Implementation -

Models:

UCS - Uniform Cost Search (Djikstra). Priority Queue
DFS - Greedy Depth First Search. Priority Stack

'''

from node import Node

frontier: any = []


class Frontier:

    def __init__(self, root: Node):
        self.frontier = [root]

    def append(self, nodes):
        self.frontier.append(nodes)

    def pop(self) -> Node:
        return self.frontier.pop()
