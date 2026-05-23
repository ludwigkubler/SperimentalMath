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

def generate_random_monotone_function(n):
    return [random.choice([0, 1]) for _ in range(2**n - 1)]

def matrix_from_function(f, n):
    A = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if f[i] == f[j]:
                A[i][j] = 1
    return A

def tropical_hermitian_rank(A):
    n = len(A)
    rank = 0
    while True:
        found_nonzero = False
        for i in range(n):
            if any(A[i][j] != 0 for j in range(n)):
                pivot_row = i
                found_nonzero = True
                break
        if not found_nonzero:
            return rank
        rank += 1
        for j in range(n):
            if A[pivot_row][j] != 0:
                for k in range(n):
                    A[k][j] = max(A[k][j], A[k][pivot_row] + A[pivot_row][j])

def communication_complexity(f, n):
    def simulate_protocol():
        x = random.randint(0, 2**n - 1)
        y = random.randint(0, 2**n - 1)
        return f[x] == f[y]
    
    success_count = 0
    for _ in range(100):  # Run multiple trials to estimate the probability
        if simulate_protocol():
            success_count += 1
    return success_count / 100

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_monotone_function(n)
        A = matrix_from_function(f, n)
        rank = tropical_hermitian_rank(A)
        cost = communication_complexity(f, n)
        
        if rank == 0 or cost == 0:
            continue
        
        results.append((rank, cost))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    ranks = [r for r, _ in results]
    costs = [c for _, c in results]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_cost = sum(costs) / len(costs)
    
    correlation_coefficient = (sum((r - mean_rank) * (c - mean_cost) for r, c in results) /
                               math.sqrt(sum((r - mean_rank)**2 for r in ranks) *
                                         sum((c - mean_cost)**2 for c in costs)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")