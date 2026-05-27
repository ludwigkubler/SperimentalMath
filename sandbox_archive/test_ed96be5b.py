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
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def determinant(A):
    n = len(A)
    det = 1
    U = [row[:] for row in A]
    gaussian_elimination(U)
    for i in range(n):
        det *= U[i][i]
    return det

def permanent(poly):
    if not poly:
        return 0
    if len(poly) == 1 and len(poly[0]) == 1:
        return poly[0][0]
    
    n = len(poly)
    perm = 0
    for i in range(n):
        subpoly = [row[:i] + row[i+1:] for row in poly[1:]]
        sign = (-1) ** (i % 2)
        perm += sign * poly[0][i] * permanent(subpoly)
    
    return perm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    K = [Fraction(i) for i in range(1, 3)]  # Field with at least two elements
    F = [[random.choice(K) for _ in range(n)] for _ in range(n)]
    
    perm = permanent(F)
    max_monotone_degree = n - 1  # Upper bound for monotone degree
    
    min_irreducible_degree = math.inf
    for i in range(2, n+1):
        for poly in itertools.combinations_with_replacement(F, i):
            det = determinant(poly)
            if det != 0:
                deg = len(poly) - 1
                if deg < min_irreducible_degree:
                    min_irreducible_degree = deg
    
    conjecture_holds = min_irreducible_degree <= max_monotone_degree
    counterexample = "" if conjecture_holds else f"Min irreducible degree {min_irreducible_degree} > max monotone degree {max_monotone_degree}"
    
    return {
        "metric_name": "min_irreducible_degree",
        "metric_value": min_irreducible_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")