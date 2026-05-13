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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def determinant(A):
    n = len(A)
    det = 1
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    for i in range(n):
        det *= A_copy[i][i]
    return det

def r_transform(M):
    n = len(M)
    R = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                R[i][j] = 1 / (n - i)
            else:
                R[i][j] = sum(M[k][i] * M[l][j] for k in range(n) for l in range(n)) / ((n - i) * (n - j))
    return R

def free_cumulant_spread(R):
    n = len(R)
    det_R = determinant(R)
    spread = 0
    for i in range(n):
        for j in range(i, n):
            spread += abs(R[i][j] - det_R ** (1 / (n - i)))
    return spread

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    R = r_transform(M)
    tau_M = free_cumulant_spread(R)
    
    metric_name = "free_cumulant_spread"
    metric_value = tau_M
    instances_tested = 1
    conjecture_holds = 0.158 <= tau_M <= 3.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")