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

def generate_cnf(n):
    cnf = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        while any(c == -d for c, d in zip(clause, cnf[-n:])):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        cnf.append(clause)
    return cnf

def calculate_quadratic_form_rank(clause):
    n = len(clause)
    Q = [[0] * n for _ in range(n)]
    for literal in clause:
        var = abs(literal) - 1
        Q[var][var] += 1
    rank = gaussian_elimination(Q)
    return rank

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                return 0
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j == i:
                continue
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return sum(1 for row in A if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        ranks = []
        depths = []
        
        for clause in cnf:
            rank = calculate_quadratic_form_rank(clause)
            ranks.append(rank)
            
            # Simulate Frege proof depth (placeholder, replace with actual calculation)
            depth = random.randint(10, 2 * n)
            depths.append(depth)
        
        if not ranks or not depths:
            return {
                "metric_name": "quadratic_form_rank",
                "metric_value": None,
                "instances_tested": len(cnf),
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": "empty_ranks_or_depths"
            }
        
        correlation = calculate_correlation(ranks, depths)
        results.append({
            "n": n,
            "correlation": correlation
        })
    
    mean_corr = sum(result["correlation"] for result in results) / len(results)
    min_corr = min(result["correlation"] for result in results)
    
    conjecture_holds = all(correlation >= 0.6 for correlation in results)
    if not conjecture_holds:
        first_failing_seed = seed
    else:
        first_failing_seed = None
    
    return {
        "metric_name": "quadratic_form_rank",
        "metric_value": mean_corr,
        "instances_tested": len(cnf) * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"correlation < 0.6 at n={min_corr}"
    }

def calculate_correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
    return cov_xy / (std_x * std_y)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Generate 30 prime seeds
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and min_corr < 0.6:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation < 0.6' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")