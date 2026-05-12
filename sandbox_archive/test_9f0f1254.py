# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    aug_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(aug_matrix[j][i]) > abs(aug_matrix[max_row][i]):
                max_row = j
        aug_matrix[i], aug_matrix[max_row] = aug_matrix[max_row], aug_matrix[i]
        pivot = aug_matrix[i][i]
        for j in range(i, n+1):
            aug_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = aug_matrix[j][i]
                for k in range(i, n+1):
                    aug_matrix[j][k] -= factor * aug_matrix[i][k]
    return [row[-1] for row in aug_matrix]

def matroid_rank(clauses):
    variables = set()
    for clause in clauses:
        variables.update(clause)
    variable_to_clauses = {v: [] for v in variables}
    for i, clause in enumerate(clauses):
        for v in clause:
            variable_to_clauses[v].append(i)
    
    max_rank = 0
    for subset_size in range(1, len(variables) + 1):
        for subset in combinations(variables, subset_size):
            independent_clauses = []
            for v in subset:
                independent_clauses.extend(variable_to_clauses[v])
            if len(set(independent_clauses)) == len(independent_clauses):
                max_rank = subset_size
    return max_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(random.randint(n * 2, n * 3)):
        clause = tuple(sorted(random.sample(range(n), 3)))
        if clause not in clauses:
            clauses.append(clause)
    
    rank = matroid_rank(clauses)
    seed_length = len(gaussian_elimination([[1] * n for _ in range(rank)], [0] * rank))
    
    return {
        "metric_name": "seed_length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": seed_length <= rank,
        "counterexample": "" if seed_length <= rank else f"Seed {seed} failed with rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i, j, k in combinations(range(10), 3)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r for r in results if not r["conjecture_holds"])["seed"]
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")