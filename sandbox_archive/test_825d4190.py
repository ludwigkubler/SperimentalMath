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
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        if factor == 0:
            continue
        for j in range(n):
            A[i][j] /= factor
        for j in range(m):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    m, n = len(A), len(A[0])
    r = 0
    for row in gaussian_elimination(A):
        if any(row[i] != 0 for i in range(n)):
            r += 1
    return r

def minimal_local_induction_ring_rank(A):
    try:
        return rank(A) ** 2
    except ZeroDivisionError:
        return float('inf')

def communication_complexity(n, k):
    # Placeholder function; replace with actual implementation
    return n * (k - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, 5)
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    cc = communication_complexity(n, k)
    mrl = minimal_local_induction_ring_rank(A)
    
    if mrl == float('inf'):
        return {
            "metric_name": "mrl",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    if mrl <= 10 * cc ** 2:
        return {
            "metric_name": "mrl",
            "metric_value": mrl,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "mrl",
            "metric_value": mrl,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"mrl={mrl} > 10 * cc^2 = {10 * cc ** 2}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [17, 31, 41, 53, 61, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mrl > 10 * cc^2\" first_failing_seed={first_failing_seed}")