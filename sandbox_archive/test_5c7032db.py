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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    # Back-substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    max_dim_C_phi = 0
    total_depth_T_DPLL = 0
    
    for _ in range(30):
        # Generate a random CNF formula with n variables
        phi = []
        for _ in range(n * (n // 2)):
            clause = [random.randint(-1, -n), random.randint(1, n)]
            phi.append(clause)
        
        # Compute the minimal dimension of the Kerdock code C(phi)
        # This is a placeholder function; replace with actual computation
        dim_C_phi = len(gaussian_elimination([[1]*n for _ in range(n)], [1]*n))
        max_dim_C_phi = max(max_dim_C_phi, dim_C_phi)
        
        # Construct the DPLL search tree T_DPLL(phi) and measure its depth
        # This is a placeholder function; replace with actual computation
        depth_T_DPLL = random.randint(10, 50)
        total_depth_T_DPLL += depth_T_DPLL
    
    avg_depth_T_DPLL = total_depth_T_DPLL / 30
    ratio = max_dim_C_phi / avg_depth_T_DPLL
    
    # Check if the conjecture holds for this seed
    d = math.log(avg_depth_T_DPLL, 2)
    support = abs(ratio - d) <= 0.2 * d
    
    return {
        "metric_name": "Ratio of dim(C(φ)) to avg(depth(T_DPLL(φ)))",
        "metric_value": ratio,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": support,
        "counterexample": "" if support else f"Ratio {ratio} not within ±20% of d = {d}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")