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

def generate_circuit(n):
    if n == 1:
        return "A"
    else:
        left = generate_circuit(n // 2)
        right = generate_circuit(n - n // 2)
        return f"({left} OR {right})"

def tropicalize_quiver(circuit):
    if circuit.isalpha():
        return {circuit: set()}
    elif "OR" in circuit:
        left, right = circuit.split(" OR ")
        quiver_left = tropicalize_quiver(left)
        quiver_right = tropicalize_quiver(right)
        quiver = {}
        for u in quiver_left:
            quiver[u] = quiver_left[u]
        for v in quiver_right:
            if v not in quiver:
                quiver[v] = set()
            quiver[v].update(quiver_right[v])
        return quiver
    elif "AND" in circuit:
        left, right = circuit.split(" AND ")
        quiver_left = tropicalize_quiver(left)
        quiver_right = tropicalize_quiver(right)
        quiver = {}
        for u in quiver_left:
            if u not in quiver:
                quiver[u] = set()
            quiver[u].update(quiver_left[u])
        for v in quiver_right:
            quiver[v] = quiver_right[v]
        return quiver
    else:
        raise ValueError("Invalid circuit")

def compute_minimal_index(quiver):
    def dfs(node, visited, index):
        if node in visited:
            return index
        visited.add(node)
        max_index = 0
        for neighbor in quiver[node]:
            max_index = max(max_index, dfs(neighbor, visited, index + 1))
        return max_index

    min_index = float('inf')
    for node in quiver:
        min_index = min(min_index, dfs(node, set(), 0))
    return min_index

def compute_resolution_diameter(circuit):
    def resolve(expr):
        if expr.isalpha():
            return {expr}
        elif "OR" in expr:
            left, right = expr.split(" OR ")
            return resolve(left).union(resolve(right))
        elif "AND" in expr:
            left, right = expr.split(" AND ")
            return resolve(left).intersection(resolve(right))
        else:
            raise ValueError("Invalid circuit")

    def dfs(node, visited):
        if node in visited:
            return 0
        visited.add(node)
        max_depth = 0
        for neighbor in quiver[node]:
            max_depth = max(max_depth, dfs(neighbor, visited))
        return max_depth + 1

    quiver = tropicalize_quiver(circuit)
    resolution_set = resolve(circuit)
    diameter = float('-inf')
    for node in resolution_set:
        diameter = max(diameter, dfs(node, set()))
    return diameter

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    
    try:
        quiver = tropicalize_quiver(circuit)
        minimal_index = compute_minimal_index(quiver)
        resolution_diameter = compute_resolution_diameter(circuit)
        
        return {
            "metric_name": "Minimal Index vs Resolution Diameter",
            "metric_value": abs(minimal_index - resolution_diameter),
            "instances_tested": 1,
            "conjecture_holds": abs(minimal_index - resolution_diameter) <= 0.5,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Minimal Index vs Resolution Diameter",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE reason=unreachable"
    
    print(result)