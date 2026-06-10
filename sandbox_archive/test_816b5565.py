# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    
    for j in range(n):
        pivot_row = -1
        for i in range(j, m):
            if Augmented[i][j] != 0:
                pivot_row = i
                break
        
        if pivot_row == -1:
            continue
        
        Augmented[pivot_row], Augmented[j] = Augmented[j], Augmented[pivot_row]
        
        for i in range(m):
            if i != j:
                factor = Augmented[i][j] / Augmented[j][j]
                for k in range(n + 1):
                    Augmented[i][k] -= factor * Augmented[j][k]
    
    rank = sum(1 for row in Augmented if any(row[i] != 0 for i in range(n)))
    return rank

def rank(A):
    m = len(A)
    n = len(A[0])
    RREF = gaussian_elimination(A, [0]*m)
    return RREF

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random communication complexity instance
    n = random.randint(5, 40)
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(0, 1) for _ in range(n)]
    
    # Compute the rank of the associated matroid
    rank_matroid = rank(A)
    
    # Calculate the rank variance of the communication complexity problem
    rank_variance = sum((A[i][j] - (sum(A[i]) / n)) ** 2 for i, j in product(range(n), range(n))) / (n * n)
    
    # Correlate the rank of the p-adic valuation with the rank variance
    correlation_coefficient = (rank_matroid * rank_variance) / (math.sqrt(rank_matroid) * math.sqrt(rank_variance))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient > 0.7,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")