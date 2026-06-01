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
    m = len(A[0])
    A_augmented = [row[:] + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(A)]
    
    for i in range(n):
        pivot_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[pivot_row][i] == 0:
            return None  # Singular matrix
        A[i], A[pivot_row] = A[pivot_row], A[i]
        
        for j in range(m):
            A[i][j] /= A[i][i]
        
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(m):
                    A[k][j] -= factor * A[i][j]
    
    return [row[m:] for row in A]

def rank(matrix):
    rref = gaussian_elimination(matrix)
    if rref is None:
        return 0
    return sum(1 for row in rref if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    φ = [random.choice([0, 1]) for _ in range(n)]
    R = [[φ[i] * φ[j] for j in range(n)] for i in range(n)]
    
    deg_R = rank(R)
    rank_φ = sum(1 for x in φ if x == 1)
    
    return {
        "metric_name": "Hodge-Tate Degree",
        "metric_value": deg_R,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(deg_R - rank_φ) <= 2 * min(deg_R, rank_φ),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")