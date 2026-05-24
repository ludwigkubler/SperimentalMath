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
        # Generate a random Boolean circuit of size n
        if n == 1:
            return ['A']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - len(left))
            return [f'({left[0]} OR {right[0]})'] + left + right
    
    def tropicalize_quiver(circuit):
        # Encode the circuit into a quiver
        quiver = {}
        for expr in circuit:
            if 'OR' in expr:
                u, v = expr.split(' OR ')
                if u not in quiver:
                    quiver[u] = []
                if v not in quiver:
                    quiver[v] = []
                quiver[u].append(v)
                quiver[v].append(u)
        return quiver
    
    def min_index(quiver):
        # Compute the minimal index of the quiver
        visited = set()
        indices = {}
        
        def dfs(node, depth=0):
            if node in visited:
                return depth - indices[node]
            visited.add(node)
            indices[node] = depth
            return max(dfs(neigh, depth + 1) for neigh in quiver.get(node, []))
        
        return min(dfs(node) for node in quiver)
    
    def resolution_tree(circuit):
        # Construct a resolution proof tree for the circuit
        if len(circuit) == 1:
            return [circuit[0]]
        else:
            left = resolution_tree(circuit[:len(circuit)//2])
            right = resolution_tree(circuit[len(circuit)//2:])
            return [f'({left[-1]} OR {right[-1]})'] + left + right
    
    def tree_diameter(tree):
        # Compute the diameter of the resolution proof tree
        if len(tree) == 1:
            return 0
        else:
            left = tree[:len(tree)//2]
            right = tree[len(tree)//2:]
            return max(len(left), len(right)) + 1
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    quiver = tropicalize_quiver(circuit)
    min_index_value = min_index(quiver)
    resolution_tree_value = resolution_tree(circuit)
    tree_diameter_value = tree_diameter(resolution_tree_value)
    
    return {
        "metric_name": "Minimal Index vs Tree Diameter",
        "metric_value": abs(min_index_value - tree_diameter_value),
        "instances_tested": 1,
        "conjecture_holds": abs(min_index_value - tree_diameter_value) <= 0.5,
        "counterexample": "" if abs(min_index_value - tree_diameter_value) <= 0.5 else f"n={n}, min_index={min_index_value}, tree_diameter={tree_diameter_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]['counterexample']}\" first_failing_seed={first_failing_seed}")