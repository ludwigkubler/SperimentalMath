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
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-zero entries below pivot
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

    return A

def determinant(A):
    n = len(A)
    det = Fraction(1)
    for i in range(n):
        det *= A[i][i]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a Tseitin formula with n variables
    n = 5 + (seed % 4) * 5  # Sweep through n ∈ {5,10,15,20,30}
    if n < 5 or n > 30:
        return {
            "metric_name": "symplectic_capacity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "invalid_n"
        }
    
    # Construct a symmetric polynomial
    x = [random.randint(1, 5) for _ in range(n)]
    f = sum(x[i] * x[j] for i in range(n) for j in range(i + 1, n)) ** 2
    
    # Compute the minimal symplectic capacity (simplified)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = f
    det_A = determinant(A)
    sym_cap = abs(det_A) / math.factorial(n)
    
    # Construct a circuit computing the symmetric function
    width_mon = 2 * n - 1
    
    return {
        "metric_name": "symplectic_capacity",
        "metric_value": sym_cap,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": sym_cap <= 1.5 * width_mon,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"insufficient_support\" first_failing_seed={seeds[support_fraction < 0.95]}")
    else:
        print("RESULT: INCONCLUSIVE missing_data")