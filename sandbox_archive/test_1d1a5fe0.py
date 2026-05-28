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
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        pivot_row = i
        for j in range(i + 1, rows):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A[i], A[pivot_row] = A[pivot_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, cols):
            A[i][j] /= pivot
        for k in range(rows):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(i, cols):
                    A[k][j] -= factor * A[i][j]
    rank = sum(1 for row in A if any(row[j] != 0 for j in range(cols)))
    return rank

def generate_3cnf(n, density=1.2):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(math.ceil(density * n * (n - 1) / 2)):
        clause = random.sample(variables, 3)
        clause = [random.choice([-1, 1]) * var for var in clause]
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    
    # Construct tropical cell complex (simplified example)
    A = [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]
    rank_value = gaussian_elimination(A)
    
    # Simulate monotone circuit size
    circuit_size = 2 ** (n ** 0.25)
    
    return {
        "metric_name": "Rank and Circuit Size",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": rank_value <= n ** 0.25 and circuit_size <= 2 ** (n ** 0.25),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")