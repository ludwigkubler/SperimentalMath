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

def generate_random_graph(n: int) -> list:
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def simplicial_homology(graph: list) -> int:
    n = len(graph)
    beta_1 = 0
    
    # Find all edges (1-simplices)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if graph[i][j] == 1]
    
    # Find all triangles (2-simplices)
    triangles = []
    for i, j, k in combinations(range(n), 3):
        if graph[i][j] == 1 and graph[j][k] == 1 and graph[k][i] == 1:
            triangles.append((i, j, k))
    
    # Calculate beta_1
    beta_1 = len(edges) - len(triangles)
    
    return beta_1

def resolution_length(graph: list) -> int:
    n = len(graph)
    clauses = []
    for i in range(n):
        clause = [j + 1 if graph[i][j] == 0 else -(j + 1) for j in range(n)]
        clauses.append(clause)
    
    length = 0
    while clauses:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            break
        literal = abs(unit_clause[0])
        clauses = [c for c in clauses if literal not in c and -literal not in c]
        length += 1
    
    return length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    
    beta_1 = simplicial_homology(graph)
    if beta_1 < 1:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "beta_1(G) < 1"
        }
    
    resolution_len = resolution_length(graph)
    if resolution_len < 2 ** beta_1:
        return {
            "metric_name": "resolution_length",
            "metric_value": resolution_len,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Resolution length {resolution_len} is less than 2^{beta_1}"
        }
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")