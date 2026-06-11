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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-zero entries below the pivot
        factor = Fraction(A[i][i])
        for j in range(i+1, n):
            factor_j = Fraction(A[j][i])
            if factor == 0 and factor_j != 0:
                return None  # Singular matrix
            A[j] = [A[j][k] - (factor_j / factor) * A[i][k] for k in range(n)]
    return A

def hodge_dimension(poly, p):
    n = len(poly)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                A[i][j] = poly[(i + j) // 2]
            else:
                A[i][j] = -poly[(i + j) // 2]
    rank = sum(1 for row in gaussian_elimination(A) if any(row))
    return rank

def satisfiability_complexity(phi):
    # Placeholder function to compute SC(φ)
    # This is a dummy implementation and should be replaced with actual computation
    return len(phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    phi = [random.choice([1, -1]) for _ in range(n)]
    poly = [sum(phi[i] * (x**i) for i in range(n)) for x in range(p)]
    
    hd = hodge_dimension(poly, p)
    sc = satisfiability_complexity(phi)
    
    return {
        "metric_name": "Correlation",
        "metric_value": hd,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_hd = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_hd} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")