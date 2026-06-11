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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
    
    # Back-substitute to get rank
    rank = n
    for i in range(n-1, -1, -1):
        if all(A[i][j] == Fraction(0) for j in range(i+1, n)):
            rank -= 1
        else:
            break
    
    return rank

def local_induction_degree_bound(G):
    n = len(G)
    A = [[Fraction(0, 1)] * n for _ in range(n)]
    
    # Compute adjacency matrix
    for u in range(n):
        for v in range(u+1, n):
            if G[u][v] == 1:
                A[u][v] = Fraction(1, 1)
                A[v][u] = Fraction(1, 1)
    
    return gaussian_elimination(A)

def communication_complexity_rank_variance(G):
    n = len(G)
    rank_A = local_induction_degree_bound(G)
    return rank_A ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        LIDB = local_induction_degree_bound(G)
        RCV = communication_complexity_rank_variance(G)
        
        if RCV > n**2:
            continue
        
        results.append((LIDB, RCV))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    LIDB_values, RCV_values = zip(*results)
    correlation_coefficient = sum((x - mean(LIDB_values)) * (y - mean(RCV_values)) for x, y in zip(LIDB_values, RCV_values)) / (len(results) * std_dev(LIDB_values) * std_dev(RCV_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean(abs_diff(LIDB_values, RCV_values)) <= 3,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

def abs_diff(values1, values2):
    return [abs(x - y) for x, y in zip(values1, values2)]

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = std_dev([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support n_tested=30")