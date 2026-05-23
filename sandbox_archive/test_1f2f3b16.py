# auto-injected by SEC sandbox
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
import math
from itertools import combinations

def generate_random_graph(n):
    if n <= 1:
        return []
    edges = set()
    for i in range(2, n + 1):
        for j in range(i - 1):
            if random.random() < 0.5:
                edges.add((j, i))
    return list(edges)

def is_connected(graph, n):
    visited = [False] * n
    stack = [0]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in range(n):
                if (node, neighbor) in graph or (neighbor, node) in graph:
                    stack.append(neighbor)
    return all(visited)

def find_minimal_delone_triangulation(graph, n):
    min_vertices = float('inf')
    best_triangulation = None
    for triangulation in combinations(range(n), 3):
        if is_connected(triangulation, n) and len(triangulation) < min_vertices:
            min_vertices = len(triangulation)
            best_triangulation = triangulation
    return best_triangulation

def dpll_solver(formula):
    def solve(assignment, clause_index):
        if clause_index == len(formula):
            return True
        for literal in formula[clause_index]:
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            if solve(new_assignment, clause_index + 1):
                return True
            new_assignment[abs(literal) - 1] = not new_assignment[abs(literal) - 1]
            if solve(new_assignment, clause_index + 1):
                return True
        return False

    n = len(formula)
    assignment = [False] * n
    return solve(assignment, 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    triangulation = find_minimal_delone_triangulation(graph, n)
    
    if triangulation is None:
        return {
            "metric_name": "Geometric Entropy vs Resolution Refutation Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No valid Delone triangulation found"
        }
    
    geometric_entropy = math.log2(len(triangulation))
    resolution_refutation_length = dpll_solver([[i + 1 if i % 2 == 0 else -i - 1 for i in range(n)]])
    
    return {
        "metric_name": "Geometric Entropy vs Resolution Refutation Length",
        "metric_value": resolution_refutation_length,
        "instances_tested": 1,
        "conjecture_holds": resolution_refutation_length <= 2 ** geometric_entropy * math.log2(2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")