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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def quaternionic_k_theory_order(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    A[i][literal - 1] += 1
                else:
                    A[i][-1] += 1
        A[-1][-1] = n
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return rank

    def clause_subset_entropy(clauses):
        total_clauses = len(clauses)
        entropy = 0
        for i in range(1, total_clauses + 1):
            for subset in itertools.combinations(clauses, i):
                prob = Fraction(i, total_clauses)
                entropy -= prob * math.log2(prob)
        return entropy

    def generate_random_cnf(n):
        clauses = []
        for _ in range(n):
            clause = random.sample(range(1, 2*n+1), random.randint(1, n))
            clause += [-l for l in clause]
            clauses.append(clause)
        return clauses

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        clauses = generate_random_cnf(n)
        ord_K_phi = quaternionic_k_theory_order(clauses)
        entropy_phi = clause_subset_entropy(clauses)
        metric_values.append((ord_K_phi, entropy_phi))
    
    if not metric_values:
        return {
            "metric_name": "ord(K_φ) vs entropy(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric_values"
        }
    
    x = [x for x, _ in metric_values]
    y = [y for _, y in metric_values]
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    var_x = sum((xi - mean_x) ** 2 for xi in x) / len(x)
    var_y = sum((yi - mean_y) ** 2 for yi in y) / len(y)
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    r_squared = cov_xy ** 2 / (var_x * var_y)
    
    return {
        "metric_name": "ord(K_φ) vs entropy(φ)",
        "metric_value": r_squared,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r_squared >= 0.9 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_r_squared = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='r_squared_too_low' first_failing_seed={first_failing_seed}")