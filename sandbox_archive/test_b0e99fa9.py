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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        denom = A[i][i]
        for j in range(n):
            A[i][j] /= denom
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def min_rank(A):
    reduced_A = gaussian_elimination(A)
    rank = sum(1 for row in reduced_A if any(val != 0 for val in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n, k = random.randint(5, 40), random.randint(2, min(n-1, 5))  # Ensure k < n
    A = [[random.choice([-1, 0, 1]) for _ in range(n)] for _ in range(n)]
    
    tropical_A = []
    for row in A:
        max_abs_val = max(abs(val) for val in row)
        tropical_row = [Fraction(val, max_abs_val) if val != 0 else Fraction(0, 1) for val in row]
        tropical_A.append(tropical_row)
    
    min_rank_value = min_rank(tropical_A)
    depth_bound = math.ceil(n**(k/4))
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank_value,
        "instances_tested": 1,
        "conjecture_holds": min_rank_value >= depth_bound and abs(min_rank_value - depth_bound) <= 2,
        "counterexample": "" if min_rank_value >= depth_bound else f"min_rank={min_rank_value}, expected at least {depth_bound}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank below expected\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")