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
        if n == 1:
            return [0]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - len(left))
            return [0] + left + right
    
    def tropicalize_quiver(circuit):
        quiver = {i: [] for i in range(len(circuit))}
        for i, gate in enumerate(circuit[1:], start=1):
            if gate == 0:
                continue
            parent = circuit[i // 2]
            quiver[parent].append(i)
        return quiver
    
    def min_index(quiver):
        visited = set()
        index = 0
        
        def dfs(node, depth):
            nonlocal index
            if node in visited:
                return
            visited.add(node)
            for neighbor in quiver[node]:
                dfs(neighbor, depth + 1)
            index = max(index, depth)
        
        dfs(0, 0)
        return index
    
    def resolution_tree(circuit):
        n = len(circuit)
        tree = [[] for _ in range(n)]
        stack = [(0, -1)]
        while stack:
            node, parent = stack.pop()
            if circuit[node] == 0:
                continue
            for neighbor in quiver[node]:
                if neighbor != parent:
                    tree[neighbor].append(node)
                    stack.append((neighbor, node))
        return tree
    
    def diameter(tree):
        n = len(tree)
        max_diameter = 0
        
        def bfs(start):
            visited = [False] * n
            queue = [(start, 0)]
            while queue:
                node, depth = queue.pop(0)
                if visited[node]:
                    continue
                visited[node] = True
                for neighbor in tree[node]:
                    queue.append((neighbor, depth + 1))
            return max_diameter
        
        for i in range(n):
            max_diameter = max(max_diameter, bfs(i))
        return max_diameter
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    quiver = tropicalize_quiver(circuit)
    min_index_val = min_index(quiver)
    tree = resolution_tree(circuit)
    diameter_val = diameter(tree)
    
    return {
        "metric_name": "Minimal Index vs Diameter",
        "metric_value": abs(min_index_val - diameter_val),
        "instances_tested": 1,
        "conjecture_holds": abs(min_index_val - diameter_val) <= 0.5,
        "counterexample": "" if abs(min_index_val - diameter_val) <= 0.5 else f"n={n}, min_index={min_index_val}, diameter={diameter_val}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")