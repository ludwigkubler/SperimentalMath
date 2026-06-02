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
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        if A[i][i] == 0:
            return 0
        det *= A[i][i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return det

def minimal_geometric_entropy(A):
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix must be non-singular")
    return math.log(abs(det_A))

def communication_complexity_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if all(x == 0 for x in A[i]):
            continue
        rank += 1
        for j in range(n):
            if A[j][i] != 0:
                for k in range(n):
                    A[j][k] -= A[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    try:
        mge_A = minimal_geometric_entropy(A)
        ccr_A = communication_complexity_rank(A)
        
        return {
            "metric_name": "mge_over_ccr",
            "metric_value": mge_A / ccr_A,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": mge_A >= 0.8 * ccr_A and mge_A <= 3,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "mge_over_ccr",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")