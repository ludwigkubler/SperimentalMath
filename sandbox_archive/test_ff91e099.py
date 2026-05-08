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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(rank, m):
            if A[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        for j in range(n):
            if j != i and A[rank][j] != 0:
                factor = A[j][i] / A[rank][i]
                for k in range(n):
                    A[j][k] -= factor * A[rank][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    q = 2
    A = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(0, q-1) for _ in range(n)]
    
    # Solve the system of linear equations
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    rank = gaussian_elimination(augmented_matrix)
    
    # Count the number of solutions
    free_vars = n - rank
    if free_vars < 0:
        S = 0
    else:
        S = q ** free_vars
    
    # Estimate the minimal ACC^0 circuit size
    if S == 0:
        circuit_size = 0
    else:
        circuit_size = math.ceil(math.log(S, 2))
    
    # Check the conjecture
    conjecture_holds = circuit_size >= math.log(S, 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE mapping_undefined"
    
    print(result)