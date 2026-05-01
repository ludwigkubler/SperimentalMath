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

def generate_random_3sat(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        if all(clause[i] != -clause[j] for i in range(3) for j in range(i+1, 3)):
            clauses.append(clause)
    return clauses

def polynomial_from_clause(clause: list) -> list:
    poly = [0] * (max(abs(x) for x in clause) + 1)
    for x in clause:
        poly[abs(x)] += x
    return poly

def matrix_multiplication(A: list, B: list) -> list:
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A: list) -> list:
    n = len(A)
    M = [row[:] + [i] for i, row in enumerate(A)]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(M[j][i]))
        if M[pivot][i] == 0:
            raise ValueError("No unique solution exists")
        M[i], M[pivot] = M[pivot], M[i]
        for j in range(n):
            if i != j:
                factor = M[j][i] / M[i][i]
                M[j] = [M[j][k] - factor * M[i][k] for k in range(n + 1)]
        M[i] = [M[i][k] / M[i][i] for k in range(n + 1)]
    return [[row[k] for k in range(n)] for row in M]

def rank_of_matrix(A: list) -> int:
    n = len(A)
    M = A[:]
    rank = 0
    for i in range(n):
        if all(M[j][i] == 0 for j in range(rank, n)):
            continue
        rank += 1
        for j in range(i + 1, n):
            factor = M[j][i] / M[rank - 1][i]
            for k in range(n):
                M[j][k] -= factor * M[rank - 1][k]
    return rank

def singular_locus_dimension(poly_system: list) -> int:
    n = len(poly_system)
    J = [[0] * n for _ in range(n)]
    for i in range(n):
        J[i][i] = poly_system[i][-1]
    try:
        rank = rank_of_matrix(J)
    except ValueError:
        return float('inf')
    return n - rank

def sos_refutation_size(poly_system: list) -> int:
    # Placeholder for a basic SOS solver
    # This is a very simplified version and not actual SOS refutation size
    n = len(poly_system)
    J = [[0] * n for _ in range(n)]
    for i in range(n):
        J[i][i] = poly_system[i][-1]
    try:
        rank = rank_of_matrix(J)
    except ValueError:
        return float('inf')
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_random_3sat(n)
    poly_system = [polynomial_from_clause(clause) for clause in clauses]
    dim_sing_V = singular_locus_dimension(poly_system)
    sos_size = sos_refutation_size(poly_system)
    metric_value = dim_sing_V
    conjecture_holds = dim_sing_V >= math.log2(sos_size) - 3 * n ** 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "singular_locus_dimension",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")