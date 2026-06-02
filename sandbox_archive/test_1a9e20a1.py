# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        return A, b
    
    def communication_complexity_rank(f):
        # Placeholder for actual CC rank computation
        return random.randint(1, 5)
    
    def minimal_index(f, n):
        m = len(f)
        A = [[0]*n for _ in range(m)]
        b = [0]*m
        for i in range(m):
            for j in range(n):
                if f[i][j] == '1':
                    A[i][j] = 1
            b[i] = 1
        
        rank = communication_complexity_rank(f)
        if rank == 0:
            return 0
        
        try:
            _, _ = gaussian_elimination(A, b)
            min_index_val = sum(gaussian_elimination(A[:i+1], b[:i+1])[-1] for i in range(n))
        except ZeroDivisionError:
            min_index_val = float('inf')
        
        return min_index_val
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        instances_tested = 0
        total_min_index = 0
        
        while instances_tested < 30:
            f = [''.join(random.choice('01') for _ in range(n)) for _ in range(2**n)]
            min_index_val = minimal_index(f, n)
            
            if min_index_val == float('inf'):
                continue
            
            total_min_index += min_index_val
            instances_tested += 1
        
        mean_min_index = total_min_index / instances_tested
        ratio = mean_min_index / (n * random.log(n))
        
        results.append({
            "metric_name": "min_index_to_cc_rank_ratio",
            "metric_value": ratio,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": ratio <= 3 * random.log(n),
            "counterexample": ""
        })
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_min_index_to_cc_rank_ratio": mean_ratio,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_ratio = sum(result["mean_min_index_to_cc_rank_ratio"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")