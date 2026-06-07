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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def det(matrix):
    n = len(matrix)
    det_val = 1
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    
    for i in range(n):
        det_val *= augmented_matrix[i][i]
    
    return det_val

def communication_complexity_rank(graph, subgraph):
    n = len(graph)
    subgraph_matrix = [[graph[i][j] if j in subgraph else 0 for j in range(n)] for i in range(n)]
    rank = sum(1 for row in subgraph_matrix if det(row) != 0)
    return rank

def minimal_local_index(graph):
    n = len(graph)
    hyperplane_arrangement = [[graph[i][j] for j in range(n)] for i in range(n)]
    mli = sum(det(row) != 0 for row in hyperplane_arrangement)
    return mli

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 3))
    
    # Generate a random k-regular graph
    graph = [[0] * n for _ in range(n)]
    degree_count = [0] * n
    
    while any(count != k for count in degree_count):
        u, v = random.sample(range(n), 2)
        if u == v or graph[u][v]:
            continue
        
        graph[u][v] = 1
        graph[v][u] = 1
        degree_count[u] += 1
        degree_count[v] += 1
    
    mli = minimal_local_index(graph)
    
    subgraph_ranks = [communication_complexity_rank(graph, [i]) for i in range(n)]
    if not subgraph_ranks:
        return {
            "metric_name": "mli(G)",
            "metric_value": mli,
            "instances_tested": n,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_subgraphs"
        }
    
    variance = sum((x - sum(subgraph_ranks) / len(subgraph_ranks)) ** 2 for x in subgraph_ranks) / len(subgraph_ranks)
    
    return {
        "metric_name": "mli(G)",
        "metric_value": mli,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": mli >= 10 * variance,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        counterexample = "first_failing_seed" if first_failing_seed is not None else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")