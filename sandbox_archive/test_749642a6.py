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

def run_trial(seed: int) -> dict:
    n = 40
    random.seed(seed)
    
    # Generate a DISJOINTNESS matrix M ∈ {0,1}^{n×n}
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    while not is_disjointness(M):
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute the free cumulant spread τ(M)
    tau_M = compute_free_cumulant_spread(M)
    
    # Check if τ(M) ≥ 1/√40 and τ(M) ≤ log 40
    lower_bound = 1 / math.sqrt(n)
    upper_bound = math.log(n)
    conjecture_holds = lower_bound <= tau_M <= upper_bound
    
    return {
        "metric_name": "free_cumulant_spread",
        "metric_value": tau_M,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

def is_disjointness(M):
    n = len(M)
    for i in range(n):
        for j in range(i + 1, n):
            if sum(M[i][k] * M[j][k] for k in range(n)) > 0:
                return False
    return True

def compute_free_cumulant_spread(M):
    n = len(M)
    R_transform = [[0.0] * n for _ in range(n)]
    
    # Compute the R-transform
    for i in range(n):
        for j in range(i, n):
            if i == j:
                R_transform[i][j] = M[i][i]
            else:
                R_transform[i][j] = (M[i][j] - 1) / (1 + M[i][i])
    
    # Compute the free cumulant spread
    tau_M = 0.0
    for i in range(n):
        for j in range(i, n):
            if i == j:
                tau_M += R_transform[i][j]
            else:
                tau_M += abs(R_transform[i][j])
    
    return tau_M

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")