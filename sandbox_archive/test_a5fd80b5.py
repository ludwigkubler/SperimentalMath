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
        if A[i][i] == 0:
            for j in range(i + 1, m):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                return None  # Singular matrix
        for j in range(m):
            if i == j:
                continue
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def hodge_rank(poly):
    n = len(poly)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i][j] = 1
            else:
                A[i][j] = poly[j]
    rank = len(gaussian_elimination(A))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clause_length = random.randint(2, 40)
    variables = set(range(n))
    clauses = [set(random.sample(variables, k=clause_length)) for _ in range(10)]
    
    poly = [0] * (n + 1)
    for clause in clauses:
        term = 1
        for var in clause:
            term *= (-1) ** (random.randint(0, 1))
        for i in range(n):
            if i not in clause:
                term *= (1 - 2 * random.randint(0, 1))
        poly += [term]
    
    rank = hodge_rank(poly)
    c = 2
    threshold = c * math.log(n)
    
    return {
        "metric_name": "arithmetic_hodge_rank",
        "metric_value": rank,
        "instances_tested": 10,
        "conjecture_holds": rank <= threshold,
        "counterexample": "" if rank <= threshold else f"Rank {rank} exceeds threshold {threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.99:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds threshold\" first_failing_seed={first_failing_seed}")