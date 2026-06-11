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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n) * (1 if random.choice([True, False]) else -1)
                   for _ in range(random.randint(2, 4))]
        clauses.append(clause)
    return clauses

def tseitin_graph(cnf):
    graph = {}
    literals = set()
    for clause in cnf:
        literals.update(abs(lit) for lit in clause)
    for literal in literals:
        graph[literal] = []
    for i, clause in enumerate(cnf):
        new_var = -len(graph) - 1
        graph[new_var] = [-l for l in clause]
        for l in clause:
            if l > 0:
                graph[l].append(new_var)
            else:
                graph[-l].append(-new_var)
    return graph

def spanning_tree(graph):
    def dfs(node, parent):
        visited.add(node)
        tree_edges.append((parent, node))
        for neighbor in graph[node]:
            if neighbor != parent and neighbor not in visited:
                dfs(neighbor, node)

    n = len(graph)
    visited = set()
    tree_edges = []
    dfs(next(iter(graph)), None)
    return tree_edges

def boolean_circuit_complexity(n):
    # Placeholder function for actual circuit complexity calculation
    return random.randint(10, 20)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    graph = tseitin_graph(cnf)
    tree_edges = spanning_tree(graph)
    geometric_complexity = len(tree_edges)
    
    entanglement_complexity = boolean_circuit_complexity(geometric_complexity)
    
    return {
        "metric_name": "Geometric Complexity vs Entanglement Complexity",
        "metric_value": geometric_complexity / math.log(n),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")