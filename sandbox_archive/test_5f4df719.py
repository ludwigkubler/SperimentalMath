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
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        b[i] /= pivot
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]

def is_independent_system(A, b):
    gaussian_elimination(A, b)
    for i in range(len(b)):
        if abs(b[i]) > 1e-9:
            return False
    return True

def trivial_representation_multiplicity(P, n):
    A = [[0] * (n+1) for _ in range(n+1)]
    b = [0] * (n+1)
    for i in range(1, n+1):
        for j in range(1, n+1):
            if P[i-1][j-1] == 1:
                A[i][j] = 1
                b[j] += 1
    return is_independent_system(A, b)

def perm_n(n):
    def perm(a, i, j):
        a[i], a[j] = a[j], a[i]
    
    def generate_perms(a, start, end):
        if start == end:
            yield list(a)
        else:
            for i in range(start, end+1):
                perm(a, start, i)
                yield from generate_perms(a, start+1, end)
                perm(a, start, i)
    
    return list(generate_perms(list(range(1, n+1)), 0, n-1))

def symmetric_power(P, n):
    result = [[0] * n for _ in range(n)]
    perms = perm_n(n)
    for p in perms:
        for i in range(n):
            for j in range(n):
                if P[i][p[j]-1] == 1 and P[p[i]-1][j] == 1:
                    result[i][j] += 1
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    S_n_P = symmetric_power(P, n)
    
    try:
        multiplicity = trivial_representation_multiplicity(S_n_P, n)
    except Exception as e:
        return {
            "metric_name": "trivial_representation_multiplicity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    # Placeholder for minimal depth-3 circuit size calculation
    min_circuit_size = n * (n - 1) // 2
    
    return {
        "metric_name": "trivial_representation_multiplicity",
        "metric_value": multiplicity,
        "instances_tested": 1,
        "conjecture_holds": multiplicity == min_circuit_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_multiplicity = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_multiplicity = math.sqrt(sum((r["metric_value"] - mean_multiplicity) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_multiplicity} std={std_multiplicity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"multiplicity does not match circuit size\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")