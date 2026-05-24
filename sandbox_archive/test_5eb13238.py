# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize_quiver(circuit):
        n = len(circuit)
        quiver = {i: [] for i in range(n)}
        for i in range(n):
            if circuit[i] == 1:
                for j in range(i + 1, n):
                    quiver[i].append(j)
        return quiver
    
    def min_index(quiver):
        visited = [False] * len(quiver)
        index = 0
        
        def dfs(node, depth):
            nonlocal index
            if depth > index:
                index = depth
            visited[node] = True
            for neighbor in quiver[node]:
                if not visited[neighbor]:
                    dfs(neighbor, depth + 1)
        
        for node in range(len(quiver)):
            if not visited[node]:
                dfs(node, 0)
        return index
    
    def resolution_tree(circuit):
        n = len(circuit)
        tree = {i: [] for i in range(n)}
        stack = [0]
        while stack:
            node = stack.pop()
            for neighbor in quiver[node]:
                if circuit[neighbor] == 1:
                    tree[node].append(neighbor)
                    stack.append(neighbor)
        return tree
    
    def diameter(tree):
        n = len(tree)
        max_diameter = 0
        
        def bfs(start):
            nonlocal max_diameter
            visited = [False] * n
            queue = [(start, 0)]
            while queue:
                node, depth = queue.pop(0)
                if depth > max_diameter:
                    max_diameter = depth
                visited[node] = True
                for neighbor in tree[node]:
                    if not visited[neighbor]:
                        queue.append((neighbor, depth + 1))
        
        for i in range(n):
            bfs(i)
        return max_diameter
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    quiver = tropicalize_quiver(circuit)
    min_idx = min_index(quiver)
    tree = resolution_tree(circuit)
    tree_diam = diameter(tree)
    
    if abs(min_idx - tree_diam) > 0.5:
        return {
            "metric_name": "min_index",
            "metric_value": min_idx,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, min_idx={min_idx}, tree_diam={tree_diam}"
        }
    
    return {
        "metric_name": "min_index",
        "metric_value": min_idx,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        result_str = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result_str)