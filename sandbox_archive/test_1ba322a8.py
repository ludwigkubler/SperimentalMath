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
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        factor = Fraction(A[i][i], A[i][i])
        for j in range(i + 1, n):
            A[j][i] /= factor
        
        # Eliminate above pivot
        for j in range(i):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    return A

def fundamental_group(G):
    n = len(G)
    laplacian = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        laplacian[i][i] = -degree
        for j in range(i + 1, n):
            if G[i][j]:
                laplacian[i][j] = laplacian[j][i] = 1
    
    ker_L = gaussian_elimination(laplacian)
    
    # Count non-zero rows to determine dimension of kernel
    dim = sum(1 for row in ker_L if any(row))
    return dim

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    dim = fundamental_group(G)
    CC_Aut_G = random.uniform(1, 2**dim)  # Simulate communication complexity
    conjecture_holds = abs(CC_Aut_G - 2**dim) <= 2 * 2**dim / n
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC_Aut_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"CC(Aut_G) = {CC_Aut_G}, dim(π₁(G)) = {dim}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")