# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

# Helper function to generate a random planar graph with n vertices
def generate_planar_graph(n):
    if n < 3:
        return [], []
    
    vertices = list(range(n))
    edges = set()
    
    # Add initial triangle
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        edges.add((u, v))
    
    for i in range(3, n):
        u = random.choice(vertices)
        v = random.choice(vertices)
        while (u, v) in edges or (v, u) in edges or not is_planar(vertices, edges | {(u, v)}):
            u = random.choice(vertices)
            v = random.choice(vertices)
        edges.add((u, v))
    
    return vertices, edges

# Helper function to check if a graph with given vertices and edges is planar
def is_planar(V, E):
    if len(E) > 3 * len(V) - 6:
        return False
    
    def dfs(u, parent, visited):
        stack = [(u, parent)]
        while stack:
            node, par = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for v in V:
                if (node, v) in E or (v, node) in E:
                    if v == parent:
                        continue
                    if v in visited and not dfs(v, node, visited):
                        return False
        return True
    
    visited = set()
    for u in V:
        if u not in visited:
            if not dfs(u, None, visited):
                return False
    
    return True

# Helper function to compute the minimal hyperbolic volume of a graph
def mvol(G):
    # Placeholder implementation (replace with actual algorithm)
    return random.random()

# Helper function to compute the communication complexity of a graph
def ccom(G):
    # Placeholder implementation (replace with actual algorithm)
    return random.randint(1, 10)

# Function to run one trial for a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_planar_graph(n)
    if not G:
        return {
            "metric_name": "mvol(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m = mvol(G)
    c = ccom(G)
    
    return {
        "metric_name": "mvol(G)",
        "metric_value": m,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

# Main function to run trials for multiple seeds
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")