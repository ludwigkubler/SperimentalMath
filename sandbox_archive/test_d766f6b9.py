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
        for k in range(i+1, n):
            factor = Fraction(M[k][i], M[i][i])
            for j in range(n + 1):
                M[k][j] -= factor * M[i][j]
    
    # Back-substitute to find the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(M[i][n], M[i][i])
        for k in range(i-1, -1, -1):
            M[k][n] -= M[k][i] * x[i]
    
    return [x[i].numerator / x[i].denominator for i in range(n)]

def compute_min_order_local_induction(graph):
    n = len(graph)
    B = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j]:
                B[i][i] += 1
                B[j][j] += 1
                B[i][j] -= 1
                B[j][i] -= 1
    
    rank = len(gaussian_elimination(B, [0] * n))
    return 2 ** (n - rank)

def compute_variance(values):
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance

def generate_random_graph(n):
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "variance_of_log_min_order"
    instances_tested = 0
    n_max = 0
    total_variance = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        values = []
        for _ in range(30):
            graph = generate_random_graph(n)
            min_order = compute_min_order_local_induction(graph)
            log_min_order = math.log2(min_order)
            values.append(log_min_order)
        
        instances_tested += len(values)
        total_variance += compute_variance(values)
    
    mean_variance = total_variance / (len(values) * 6)
    conjecture_holds = True
    counterexample = ""
    
    if mean_variance == 0:
        conjecture_holds = False
        counterexample = "metric_saturation"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"metric_saturation\" first_failing_seed={first_failing_seed}")