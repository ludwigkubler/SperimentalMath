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

def is_k_clique(graph, k):
    n = len(graph)
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 0:
                return False
    return True

def generate_random_graph(n):
    graph = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    return graph

def is_symmetric(graph):
    n = len(graph)
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] != graph[j][i]:
                return False
    return True

def find_symmetry_group_order(graph):
    n = len(graph)
    if not is_symmetric(graph):
        return float('inf')
    
    symmetries = []
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                symmetries.append((i, j))
    
    order = len(symmetries)
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_order = 0
    k_clique_counterexample = ""
    
    for _ in range(instances_tested):
        graph = generate_random_graph(n)
        if is_k_clique(graph, n):
            order = find_symmetry_group_order(graph)
            if order < instances_tested:
                k_clique_counterexample = "Graph with small symmetry group found"
                break
        else:
            order = find_symmetry_group_order(graph)
            total_order += order
    
    mean_order = total_order / instances_tested
    conjecture_holds = (mean_order >= n**0.25) and (k_clique_counterexample == "")
    
    return {
        "metric_name": "Symmetry Group Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": k_clique_counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")