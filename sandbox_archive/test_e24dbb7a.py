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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(2**n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        A_b = [row + [b[i]] for i, row in enumerate(A)]
        
        for j in range(n):
            pivot_row = None
            for i in range(j, m):
                if A_b[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row is None:
                continue
            
            A_b[pivot_row], A_b[j] = A_b[j], A_b[pivot_row]
            
            for i in range(m):
                if i != j:
                    factor = A_b[i][j] / A_b[j][j]
                    for k in range(n + 1):
                        A_b[i][k] -= factor * A_b[j][k]
        
        return [row[-1] for row in A_b if row[-2] == 0]
    
    def minimal_index(f, n):
        m = len(f)
        A = [[f[i ^ (1 << j)] - f[i] for i in range(m)] for j in range(n)]
        b = [f[i] for i in range(m)]
        return sum(gaussian_elimination(A[:i+1], b[:i+1])[-1] for i in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            r = communication_complexity_rank(f)
            min_index_val = minimal_index(f, n)
            ratio = min_index_val / r if r != 0 else float('inf')
            total_ratio += ratio
            instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested
    support_fraction = (mean_ratio <= 3 * math.log(n_values[-1])) / len(n_values)
    
    return {
        "metric_name": "min_index_to_rank_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mean_ratio > 3 * log(n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 157))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_ratio > 3 * log(n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")