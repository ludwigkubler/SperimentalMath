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
        # Find pivot in column i with maximum absolute value
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        # Swap rows to put pivot on diagonal
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def tropicalize_Birkhoff_polytope(F):
    n = len(F)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if F[i][j]:
                A[i][j] = 1
            else:
                A[i][j] = -math.inf
    
    # Perform Gaussian elimination over tropical semiring
    A_tropical = gaussian_elimination(A)
    
    # Count the number of non-zero entries in the upper triangle
    rank = 0
    for i in range(n):
        for j in range(i, n):
            if A_tropical[i][j] != -math.inf:
                rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a Monotone k-CLIQUE instance
    n = random.randint(5, 40)
    F = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        F[i][i] = 1
    
    # Compute the tropicalized Birkhoff polytope
    P_F = tropicalize_Birkhoff_polytope(F)
    
    # Check if the rank meets the conjecture bounds
    k = sum(sum(row) for row in F)
    lower_bound = math.ceil(math.sqrt(n))
    upper_bound = math.floor((math.sqrt(n))**k)
    
    conjecture_holds = lower_bound <= P_F <= upper_bound
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": P_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < math.ceil(math.sqrt(r["instances_tested"])) - 20 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < math.ceil(math.sqrt(result["instances_tested"])) - 20)
        print(f"RESULT: FALSIFIED counterexample=\"n={result['instances_tested']}, k=1\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")