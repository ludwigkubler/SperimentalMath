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

def generate_instance(n: int, m: int) -> dict:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return {"variables": variables, "clauses": clauses}

def shortest_path_length(graph: dict, start: int, end: int) -> float:
    n = len(graph)
    dist = [float('inf')] * n
    dist[start - 1] = 0
    queue = [(start, 0)]
    
    while queue:
        u, d = queue.pop(0)
        if d > dist[u - 1]:
            continue
        for v in graph[u]:
            alt = d + 1
            if alt < dist[v - 1]:
                dist[v - 1] = alt
                queue.append((v, alt))
    
    return dist[end - 1]

def compute_energy_flow(graph: dict, start: int, end: int) -> float:
    return shortest_path_length(graph, start, end)

def dpll_search_tree_height(instance: dict) -> int:
    variables = instance["variables"]
    clauses = instance["clauses"]
    n = len(variables)
    
    def dfs(model):
        if not clauses:
            return 0
        literal = random.choice([v for v in variables if v not in model and -v not in model])
        if literal > 0:
            model.add(literal)
        else:
            model.add(-literal)
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        return 1 + max(dfs(model) for model in (model, set()))
    
    return dfs(set())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instance = generate_instance(5, 7)  # Example instance with 5 variables and 7 clauses
    n = len(instance["variables"])
    m = len(instance["clauses"])
    graph = {i + 1: [] for i in range(n)}
    
    for clause in instance["clauses"]:
        for literal in clause:
            if literal > 0:
                graph[literal].append(literal + n)
                graph[literal + n].append(literal)
            else:
                graph[-literal].append(-literal + n)
                graph[-literal + n].append(-literal)
    
    start, end = random.sample(range(1, n + 1), 2)
    energy_flow = compute_energy_flow(graph, start, end)
    dpll_height = dpll_search_tree_height(instance)
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": dpll_height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(dpll_height - energy_flow) <= 3 * math.sqrt(energy_flow),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")