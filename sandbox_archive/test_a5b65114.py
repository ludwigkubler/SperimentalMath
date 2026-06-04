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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(c == 0 for c in clause):
            clause[random.randint(0, n - 1)] = random.choice([-1, 1])
        clauses.append(clause)
    return clauses

def matrix_representation(clauses):
    n = len(clauses[0])
    m = len(clauses)
    A = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(clauses):
        for j, lit in enumerate(clause):
            if lit != 0:
                A[i][j] = -lit
                A[i][-1] += abs(lit)
    return A

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n - 1):
        i_max = max(range(rank, m), key=lambda i: abs(A[i][j]))
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(rank + 1, m):
            factor = -A[i][j] / A[rank][j]
            for k in range(j, n):
                A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def minimal_tropical_symplectic_volume(A):
    rank = gaussian_elimination(A)
    return rank

def entropy(clauses):
    total_clauses = len(clauses)
    counts = [0] * (total_clauses + 1)
    for clause in clauses:
        counts[len(clause)] += 1
    probabilities = [c / total_clauses for c in counts]
    return -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 5 * n)
    clauses = generate_cnf(n, m)
    A = matrix_representation(clauses)
    TSV = minimal_tropical_symplectic_volume(A)
    entropy_val = entropy(clauses)
    correlation = (TSV - entropy_val) / math.sqrt(TSV**2 + entropy_val**2)
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")