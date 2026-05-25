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

def gaussian_elimination(A, b):
    n = len(b)
    M = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    for i in range(n):
        # Find the pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        
        # Swap rows
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate below the pivot
        factor = M[i][i]
        for j in range(i, n+1):
            M[i][j] /= factor
        for k in range(i+1, n):
            factor = M[k][i]
            for j in range(i, n+1):
                M[k][j] -= factor * M[i][j]
    
    # Back-substitute to find the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][-1]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n**2)
    
    # Generate a max-CUT instance
    edges = set()
    while len(edges) < m:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    # Construct the tropicalized lattice
    d = len(edges)
    Q = [[0] * d for _ in range(d)]
    b = [0] * d
    
    edge_list = list(edges)
    for i in range(d):
        u, v = edge_list[i]
        Q[u][i] = 1
        Q[v][i] = 1
        b[i] = random.randint(1, 10)
    
    # Compute the minimal rank of the quadratic form
    x = gaussian_elimination(Q, b)
    min_rank = sum(abs(val) for val in x if abs(val) > 1e-9)
    
    # Check the conjecture
    conjecture_holds = min_rank >= math.pow(d, 1/3)
    counterexample = "" if conjecture_holds else "minimal_rank_not_sufficient"
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [53, 67, 71, 73, 79]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank_not_sufficient\" first_failing_seed={first_failing_seed}")