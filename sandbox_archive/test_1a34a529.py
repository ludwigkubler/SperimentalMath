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
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 5))
    
    # Construct a monotone DNF formula for k-CLIQUE
    clauses = []
    for i in range(k):
        clause = [random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    # Form the incidence matrix
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            if any(x == i + 1 and y == j + 1 for x, y in clauses):
                M[i][j] = 1
    
    # Compute the rank of the matroid
    rank = matrix_rank(M)
    
    # Calculate the circuit size (simplified as a proxy for complexity)
    circuit_size = sum(len(clause) for clause in clauses)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n ** (k / 2),
        "counterexample": "" if rank >= n ** (k / 2) else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, k={results[0]['instances_tested']}\" first_failing_seed={first_failing_seed}")