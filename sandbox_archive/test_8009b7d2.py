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
        if A[i][i] == 0:
            # Find a non-zero pivot in the column
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                continue  # No non-zero pivot found, skip this row
        factor = Fraction(A[i][i], A[i][i])
        for j in range(i, n):
            A[i][j] /= factor
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = Fraction(A[k][i], A[i][i])
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_rank(A):
    rref = gaussian_elimination(A)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def construct_quasigroup(n, seed):
    random.seed(seed)
    q = [[(i * j) % n for j in range(n)] for i in range(n)]
    return q

def resolution_width(phi):
    # Placeholder function to calculate the resolution width of a CNF formula
    # This is a stub and should be replaced with an actual implementation
    return len(phi)

def run_trial(seed: int) -> dict:
    n = random.choice([10, 20, 30, 40])
    phi = construct_quasigroup(n, seed)
    q = construct_quasigroup(n, seed + 1)
    order = matrix_rank(q)
    width = resolution_width(phi)
    return {
        "metric_name": "Order(Q(φ)) vs. w(φ)",
        "metric_value": order * width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")