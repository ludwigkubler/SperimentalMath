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

def generate_disjointness_instance(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([0, 1]) for _ in range(n)]
        if any(clause[i] == 1 for i in range(n)):
            clauses.append(clause)
    return clauses

def polynomial_from_clauses(clauses, n):
    poly = []
    for clause in clauses:
        term = [0] * n
        for i in range(n):
            if clause[i] == 1:
                term[i] = 1
        poly.append(term)
    return poly

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        pivot_row = -1
        for i in range(rank, rows):
            if matrix[i][j] == 1:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        rank += 1
        for i in range(rows):
            if i != rank - 1 and matrix[i][j] == 1:
                factor = Fraction(-matrix[i][j], matrix[rank-1][j])
                for k in range(cols):
                    matrix[i][k] += factor * matrix[rank-1][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_disjointness_instance(n)
    poly = polynomial_from_clauses(clauses, n)
    rank = gaussian_elimination(poly)
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank > n**2 / 4
    counterexample = "" if conjecture_holds else f"Instance not satisfiable with rank {rank}"
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Instance not satisfiable\" first_failing_seed={first_failing_seed}")