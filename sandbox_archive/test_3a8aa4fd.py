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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    instances_tested = 100
    symplectic_capacity_sum = 0
    log2_t_star_sum = 0
    
    for _ in range(instances_tested):
        f = [random.randint(0, 1) for _ in range(n)]
        t_star = sum(f)
        if t_star == 0 or t_star == n:
            continue
        
        M_f = [[f[j] ^ f[i] for j in range(n)] for i in range(n)]
        
        # Compute symplectic capacity (simplified version for demonstration)
        rank_M_f = gaussian_elimination(M_f)
        symplectic_capacity = rank_M_f
        
        symplectic_capacity_sum += symplectic_capacity
        log2_t_star_sum += math.log2(t_star)
    
    mean_symplectic_capacity = symplectic_capacity_sum / instances_tested
    mean_log2_t_star = log2_t_star_sum / instances_tested
    
    k = 1.0  # Example constant for the bound
    abs_diff = abs(mean_symplectic_capacity - mean_log2_t_star)
    
    conjecture_holds = abs_diff <= k
    counterexample = "" if conjecture_holds else f"mean_symplectic_capacity={mean_symplectic_capacity}, mean_log2_t_star={mean_log2_t_star}"
    
    return {
        "metric_name": "symplectic_capacity",
        "metric_value": mean_symplectic_capacity,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(cols):
        pivot_row = None
        for j in range(rank, rows):
            if matrix[j][i] == 1:
                pivot_row = j
                break
        
        if pivot_row is not None:
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            
            for j in range(rows):
                if j != rank - 1:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] ^= factor * matrix[rank - 1][k]
    
    return rank

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")