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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    rank = 0
    for row in gaussian_elimination(A):
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n)
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        
        r = matrix_rank(A)
        te_n_r = r * math.log2(n)  # Simplified TE(n, r) as O(r log n)
        
        results.append({
            "n": n,
            "m": m,
            "A": A,
            "r": r,
            "te_n_r": te_n_r
        })
    
    if len(results) < 30:
        return {
            "metric_name": "TE(n, r)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    te_values = [r["te_n_r"] for r in results]
    r_values = [r["r"] for r in results]
    
    mean_te = sum(te_values) / len(te_values)
    std_te = math.sqrt(sum((x - mean_te) ** 2 for x in te_values) / len(te_values))
    
    correlation_coefficient = sum((te_values[i] - mean_te) * (r_values[i] - mean(r_values)) for i in range(len(te_values))) / (len(te_values) * std_te * math.sqrt(sum((x - mean(r_values)) ** 2 for x in r_values)))
    
    return {
        "metric_name": "TE(n, r)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_te = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_te = math.sqrt(sum((r["metric_value"] - mean_te) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_te} std={std_te} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")