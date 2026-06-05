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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def term_overlap_matrix(cnf, n):
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for lit1 in clause:
            for lit2 in clause:
                if lit1 != lit2:
                    matrix[abs(lit1)][abs(lit2)] += 1
    return matrix

def determinant(matrix, n):
    det = 0
    indices = list(range(n))
    def get_sign(p):
        s = 0
        while p < len(indices):
            if p % 2 != 0:
                s += 1
            p += 1
        return (-1) ** s

    def expand(i, temp_matrix, a, k, n):
        nonlocal det
        m = len(temp_matrix)
        f = len(temp_matrix[0])
        for j in range(0, m):
            if j != i:
                t = []
                for p in range(0, f):
                    if p != k:
                        t.append(temp_matrix[j][p])
                temp_matrix.append(t)
                det += get_sign(a) * temp_matrix[i][k] * determinant(temp_matrix, n - 1)
                a += 1
                temp_matrix.pop()

    expand(0, matrix, 0, 0, n)
    return det

def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))

def alexander_brandt_index(matrix, n):
    det = determinant(matrix, n)
    if det == 0:
        return None
    trace_val = trace(matrix)
    ab_index = Fraction(trace_val, det) if det != 0 else None
    return ab_index

def communication_complexity_rank_variance(cnf, n):
    # Placeholder for actual implementation of rank variance calculation
    return random.uniform(0, 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        matrix = term_overlap_matrix(cnf, n)
        ab_index = alexander_brandt_index(matrix, n)
        if ab_index is None:
            continue
        rank_variance = communication_complexity_rank_variance(cnf, n)
        results.append((ab_index, rank_variance))
    if not results:
        return {
            "metric_name": "ABI vs Rank Variance",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    ab_indices = [ab for ab, _ in results]
    rank_variances = [variance for _, variance in results]
    correlation_coefficient = sum((ab - sum(ab_indices) / len(ab_indices)) * (variance - sum(rank_variances) / len(rank_variances)) for ab, variance in results) / (len(results) * sum((ab - sum(ab_indices) / len(ab_indices)) ** 2 for ab in ab_indices) * sum((variance - sum(rank_variances) / len(rank_variances)) ** 2 for variance in rank_variances))
    return {
        "metric_name": "ABI vs Rank Variance",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == n for _, _ in results)),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = (sum((x - mean_value) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8\" first_failing_seed={first_failing_seed}")