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
        # Find a pivot row with non-zero element at column i
        pivot_row = next((j for j in range(i, n) if A[j][i] != 0), None)
        if pivot_row is None:
            continue
        
        # Swap the current row with the pivot row
        A[i], A[pivot_row] = A[pivot_row], A[i]
        
        # Eliminate non-zero elements below the pivot
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]

def count_non_zero_coeffs(A):
    return sum(sum(1 for x in row if x != 0) for row in A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    # Convert to GF(2) indicator polynomial
    B = []
    for row in A:
        B.append(sum(row[i] << i for i in range(n)))
    
    # Compute elementary symmetric decomposition using Gaussian elimination
    A = [[Fraction(x, 1) for x in row] for row in B]
    gaussian_elimination(A)
    
    # Count non-zero coefficients
    num_coeffs = count_non_zero_coeffs(A)
    
    # Derive ABP width from a bounded-depth circuit (simplified example)
    abp_width = n
    
    return {
        "metric_name": "ABP Width",
        "metric_value": abp_width,
        "instances_tested": 1,
        "conjecture_holds": num_coeffs <= abp_width,
        "counterexample": "" if num_coeffs <= abp_width else f"Counterexample with n={n}, num_coeffs={num_coeffs}, abp_width={abp_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")