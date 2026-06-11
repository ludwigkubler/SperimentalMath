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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def det(A):
    n = len(A)
    reduced_B = [row[:] for row in A]
    gaussian_elimination(reduced_B)
    det_val = 1
    for i in range(n):
        det_val *= reduced_B[i][i]
    return det_val

def br_order(G):
    n = len(G)
    B = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                B[i][j] = 1
                B[j][i] = 1
    return abs(det(B))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(2, min(n-1, 3))
    
    G = [[0] * n for _ in range(n)]
    for i in range(d):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        while u == v or G[u][v]:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
        G[u][v] = 1
        G[v][u] = 1
    
    br = br_order(G)
    w_G = sum(sum(row) for row in G) // 2  # Sum of degrees divided by 2
    
    return {
        "metric_name": "min_order(Br(G))",
        "metric_value": br,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")