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

def generate_d_regular_graph(d, n):
    if d * n % 2 != 0:
        return None  # Graph size must be a multiple of the degree
    graph = [[] for _ in range(n)]
    edges = set()
    
    def add_edge(i, j):
        if (i, j) not in edges and (j, i) not in edges:
            graph[i].append(j)
            graph[j].append(i)
            edges.add((i, j))
            edges.add((j, i))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
    
    return graph

def calculate_mrl(graph):
    # Placeholder for mrl calculation
    return sum(len(neighbors) for neighbors in graph) / len(graph)

def generate_sat_instance(graph, variables):
    clauses = []
    for i in range(len(graph)):
        if not graph[i]:
            continue
        clause = [random.choice([1, -1]) * (i + 1)]
        for j in graph[i]:
            clause.append(random.choice([1, -1]) * (j + 1))
        clauses.append(clause)
    return clauses

def calculate_resolution_width(clauses):
    # Placeholder for resolution width calculation
    return len(max(clauses, key=len))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 8))
    graph = generate_d_regular_graph(d, n)
    if not graph:
        return {
            "metric_name": "mrl(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    mrl_G = calculate_mrl(graph)
    variables = list(range(n))
    clauses = generate_sat_instance(graph, variables)
    w_phi_G = calculate_resolution_width(clauses)
    
    return {
        "metric_name": "mrl(G)",
        "metric_value": mrl_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mrl_G >= w_phi_G,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        metric_values = [r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None]
        conjecture_holds = all(r["conjecture_holds"] for r in results)
        
        if conjecture_holds:
            mean_value = sum(metric_values) / len(metric_values)
            std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
            support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
            
            if support_fraction >= 0.8:
                print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
            else:
                print("RESULT: INCONCLUSIVE insufficient_support")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            counterexample = "mapping_undefined"  # Placeholder
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")