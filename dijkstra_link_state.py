#!/usr/bin/env python3

from collections import OrderedDict
from sortedcollections import OrderedSet

import numpy as np
import pandas as pd

import graphviz
from PIL import Image

# _____________ user input _____________

start = 'u'
V = 'uvwxyz'
E = {
    ('u', 'w'): 8,
    ('u', 'v'): 6,
    ('u', 'x'): 6,
    ('v', 'x'): 8,
    ('v', 'w'): 4,
    ('x', 'w'): 1,
    ('x', 'y'): 7,
    ('w', 'z'): 9,
    ('w', 'y'): 1,
    ('y', 'z'): 8,
}

# _____________ user input _____________

class Node:
    def __init__(self, value, dist=0, parent=None):
        self.value = value
        self.dist = dist      # the distance (cost) value toward the initiator
        self.parent = parent  # predecessor node in the spanning tree rooted at the initiator

    def __repr__(self):
        return self.value

    def __str__(self):
        return f"Node(value={self.value}, dist={self.dist}, parent={self.parent})"

    def __getitem__(self, q):
        """Returns the dist from node `p` to `q` if an edge exists; otherwise, infinity"""
        return E[(self.value, q.value)] if (self.value, q.value) in E else np.inf

graph = OrderedSet(map(lambda u: Node(value=u, parent=Node(value=start)), sorted(set(V) - set(start))))
visited = OrderedSet({Node(value=start)})  # set of nodes whose least-cost-path is definitively known
table = OrderedDict([("N'", [start])])
path = set()

# Initialization
for u in graph:
    if (start, u.value) in E:
        u.dist = E[(start, u.value)]
        table[f"D({u.value}),p({u.value})"] = [f"{u.dist},{u.parent.value}"]
    else:
        u.dist = np.inf
        table[f"D({u.value}),p({u.value})"] = [np.inf]

# Computes shortest-cost path from a node to all other nodes
for _ in range(len(V)-1):
    p = min(graph-visited, key=lambda u: u.dist)

    visited.add(p)
    path.add((p.parent.value, p.value))  # NOTE: used for graphviz
    
    table["N'"].append(''.join(map(repr, visited)))

    for q in graph:
        header = f"D({q.value}),p({q.value})"

        if q in visited or (p.value, q.value) not in E:
            table[header].append("---" if q in visited else np.inf)
            continue

        if (p.dist + p[q]) < q.dist:
            q.dist = p.dist + p[q]
            q.parent = p

        table[header].append(f"{q.dist},{q.parent.value}")

# Create graphviz digraph
sptree = graphviz.Digraph("Dijkstra's Link State Algorithm", filename='sptree')
sptree.attr(rankdir='LR')

[sptree.node(v) for v in V]
[sptree.edge(u, v, label=str(E[(u, v)]), color="Red" if (u, v) in path else None) for (u, v) in E]


# Print the computed table
print(pd.DataFrame(table).to_markdown(tablefmt="rounded_grid"))

# Open graph in system viewer
sptree.render(directory="tree-output", format="png")
img = Image.open('tree-output/sptree.png')
img.show()
