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
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for k in range(i+1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

    return A

def matrix_det(A):
    n = len(A)
    det = 1
    A = gaussian_elimination(A)
    for i in range(n):
        det *= A[i][i]
    return det

def free_entropy(P):
    n = len(P)
    eigenvalues = [matrix_det([[P[i][j] if (i != k and j != l) else 1 - P[i][j] for j in range(n)] for k in range(n)]) for i in range(n)]
    return sum(math.log(eigenvalue) for eigenvalue in eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    if n < 5 or n > 40:
        return {"metric_name": "free_entropy", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "n_out_of_range"}
    
    P = [[random.random() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        P[i][i] = 1 - sum(P[i][:i] + P[i][i+1:])
    
    chi_P = free_entropy(P)
    if chi_P is None:
        return {"metric_name": "free_entropy", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "computational_error"}
    
    return {
        "metric_name": "free_entropy",
        "metric_value": chi_P,
        "instances_tested": 1,
        "conjecture_holds": n * math.sqrt(n) * math.log(n) / (2 * n) <= chi_P <= n * math.sqrt(n) * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"free_entropy_out_of_bounds\" first_failing_seed={first_failing_seed}")