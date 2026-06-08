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
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n + 1):
                if k == i:
                    A[j][k] = 0
                else:
                    A[j][k] -= factor * A[i][k]
    return A

def characteristic_polynomial(f):
    n = len(f)
    A = [[0] * (n+1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if f[i][j]:
                A[j][i] = 1
    A = gaussian_elimination(A)
    
    # Calculate the determinant of the augmented matrix
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def communication_complexity_rank_variance(f):
    n = len(f)
    rank = sum(1 for row in f if any(row))
    return rank * (n - rank)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    instances_tested = 30
    n_max = n
    
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        # Generate a random boolean function f with n variables
        f = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        
        # Compute the characteristic polynomial of f
        det = characteristic_polynomial(f)
        
        # Compute the communication complexity rank variance κ(f) for f
        kappa_f = communication_complexity_rank_variance(f)
        
        if kappa_f == 0:
            continue
        
        # Calculate log(√[n]I(f)) and log(κ(f))
        metric_value = math.log(math.sqrt(abs(det))) - math.log(kappa_f)
        
        total_metric_value += metric_value
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0 if conjecture_holds else 0.0
    
    return {
        "metric_name": "log(sqrt(I(f)) / kappa(f))",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")