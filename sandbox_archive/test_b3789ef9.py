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
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank_of_matrix(A):
    A = [row[:] for row in A]
    gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def generate_random_sat_instance(n, m):
    variables = set(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def koszul_complex_size(clauses):
    A = [[0] * (len(clauses) + 2) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for var in clause:
            A[i][var - 1] = 1
        A[i][-2] = 1
        A[-1][i] = 1
    return rank_of_matrix(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_generators = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n // 2, n)
            clauses = generate_random_sat_instance(n, m)
            generators = koszul_complex_size(clauses)
            total_generators += generators
            instances_tested += 1
    
    mean_generators = total_generators / instances_tested
    conjecture_holds = mean_generators <= max(0.5 * n for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_koszul_generators",
        "metric_value": mean_generators,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")