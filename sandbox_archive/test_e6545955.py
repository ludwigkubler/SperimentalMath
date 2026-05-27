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
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = Fraction(A[i][i])
        for k in range(i + 1, n):
            A[k][i] /= factor
        
        # Eliminate above
        for k in range(i):
            factor = Fraction(A[k][i])
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    
    return A

def rank_of_matrix(A):
    n = len(A)
    A_augmented = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(A)]
    A_rref = gaussian_elimination(A_augmented)
    rank = sum(1 for row in A_rref if any(x != 0 for x in row[:n]))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    M = [row[:] + row for row in M]  # Symmetrize
    
    rank_F = rank_of_matrix(M)
    
    if rank_F == 0:
        return {
            "metric_name": "symplectic_rank_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rank_zero"
        }
    
    expected_ratio = math.sqrt(n) / rank_F
    
    return {
        "metric_name": "symplectic_rank_ratio",
        "metric_value": expected_ratio,
        "instances_tested": 1,
        "conjecture_holds": False if abs(expected_ratio - 1) > 0.1 else True,
        "counterexample": "" if abs(expected_ratio - 1) <= 0.1 else f"ratio={expected_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(v is not None for v in metric_values):
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        if support_fraction >= 0.9:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='{results[first_failing_seed]['counterexample']}' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE some seeds produced rank zero matrices")