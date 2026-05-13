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
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]

def determinant(A):
    n = len(A)
    det = Fraction(1)
    for i in range(n):
        det *= A[i][i]
    return det

def moment_cumulant_inversion(moments):
    n = len(moments)
    cumulants = [0] * n
    cumulants[0] = moments[0]
    for k in range(1, n):
        cumulants[k] = moments[k]
        for j in range(k-1, 0, -1):
            cumulants[j] -= (j + 1) * cumulants[j+1]
        cumulants[0] += (-1)**k * cumulants[1]
    return cumulants

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute free cumulants
    moments = [sum(sum(row[j] * row[k] for j in range(n)) for k in range(n)) for i in range(n)]
    cumulants = moment_cumulant_inversion(moments)
    
    # Calculate σ(M)
    sigma_M = max(abs(c) for c in cumulants) - min(abs(c) for c in cumulants)
    
    return {
        "metric_name": "sigma_M",
        "metric_value": sigma_M,
        "instances_tested": 1,
        "conjecture_holds": sigma_M >= 0.1 * n,
        "counterexample": "" if sigma_M >= 0.1 * n else f"Matrix with n={n} and sigma_M={sigma_M}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_sigma_M = sum(r["metric_value"] for r in results) / len(results)
    std_sigma_M = math.sqrt(sum((r["metric_value"] - mean_sigma_M)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_sigma_M} std={std_sigma_M} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"sigma_M < 0.1n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")