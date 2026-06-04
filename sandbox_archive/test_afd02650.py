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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [row[i] for i, row in enumerate(A) if all(x == 0 for x in row[:i])]
    
    def matrix_rank(A):
        return len(gaussian_elimination(A))
    
    def algebraic_K_theory(G):
        # Simplified model of K-theory generators based on rank
        return matrix_rank(G)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        r = random.randint(1, n)  # Matrix rank
        G = [[random.randint(0, 1) for _ in range(n)] for _ in range(r)]
        K0_G = algebraic_K_theory(G)
        
        if K0_G == 0 or r == 0:
            continue
        
        results.append({
            'K0': K0_G,
            'r': r
        })
    
    if len(results) < 30:
        return {
            "metric_name": "K0_over_r",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    K0_values = [result['K0'] for result in results]
    r_values = [result['r'] for result in results]
    
    mean_K0_over_r = sum(K0 / r for K0, r in zip(K0_values, r_values)) / len(results)
    std_dev_K0_over_r = math.sqrt(sum((K0 / r - mean_K0_over_r) ** 2 for K0, r in zip(K0_values, r_values)) / len(results))
    
    correlation_coefficient = sum((K0 / r - mean_K0_over_r) * (r - mean(r_values)) for K0, r in zip(K0_values, r_values)) / (len(results) * std_dev_K0_over_r * math.sqrt(sum((r - mean(r_values)) ** 2 for r in r_values)))
    
    max_abs_deviation = max(abs(K0 / r - mean_K0_over_r) for K0, r in zip(K0_values, r_values))
    
    conjecture_holds = correlation_coefficient >= 0.7 and max_abs_deviation <= 1.5
    counterexample = "" if conjecture_holds else f"K0/G = {max(K0 / r for K0, r in zip(K0_values, r_values))}, r = {max(r for _, r in zip(K0_values, r_values))}"
    
    return {
        "metric_name": "K0_over_r",
        "metric_value": mean_K0_over_r,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result['conjecture_holds'] for result in results):
        mean_value = sum(result['metric_value'] for result in results) / len(results)
        std_dev = math.sqrt(sum((result['metric_value'] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        counterexample = next(result['counterexample'] for result in results if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")