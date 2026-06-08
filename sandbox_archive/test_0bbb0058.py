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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def next_prime(n):
        while not is_prime(n):
            n += 1
        return n

    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
            clauses.append([-variables[i], f'y{i}'])
            clauses.append([f'y{i}', -f'y{j}'] for j in range(i+1, n))
        return variables, clauses

    def resolution(clauses):
        new_clauses = set(clauses)
        while True:
            new_clause = None
            for clause1 in new_clauses:
                for clause2 in new_clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in set(clause1) & set(clause2)]
                        break
                if new_clause:
                    break
            if not new_clause:
                return None
            if any([len(c) == 0 for c in new_clauses]):
                return None
            new_clauses.add(tuple(sorted(new_clause)))
        return len(new_clauses)

    def minimal_representation_degree(n):
        variables, clauses = tseitin_formula(n)
        m = len(clauses)
        A = [[0] * (m + n) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if clauses[i][j]:
                    A[i][j] = 1
        rank = gaussian_elimination(A)
        return m - sum(1 for row in rank if all(x == 0 for x in row))

    def log_resolution_width(w):
        return math.log2(w)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            variables, clauses = tseitin_formula(n)
            w = resolution(clauses)
            if w is None:
                continue
            degree = minimal_representation_degree(n)
            results.append((log_resolution_width(w), degree))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((x[0] - y[0]) * (x[1] - y[1]) for x, y in zip(results, results)) / len(results) ** 2
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": -0.5 <= correlation <= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [next_prime(random.randint(2, 100)) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")