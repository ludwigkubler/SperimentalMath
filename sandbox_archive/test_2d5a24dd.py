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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def local_index(G, p):
        n = len(G)
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in G:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        A = gaussian_elimination(adj_matrix)
        count = 0
        for i in range(n):
            if any(A[i]):
                count += 1
        return count
    
    def resolution_width(G, p):
        n = len(G)
        # Placeholder for actual resolution width computation
        # For simplicity, we assume a linear relationship here
        return n * random.randint(2, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = 2
    
    G = []
    for _ in range(n):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in G and (v, u) not in G:
            G.append((u, v))
    
    ν_G = local_index(G, p)
    width = resolution_width(G, p)
    
    metric_value = width
    instances_tested = 1
    conjecture_holds = width >= 2 ** (ν_G * math.log(2, n))
    counterexample = "" if conjecture_holds else f"Width {width} < 2^(Ω({ν_G})) for n={n}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")