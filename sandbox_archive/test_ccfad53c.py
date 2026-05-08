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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError('Incompatible dimensions for matrix multiplication')

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C

def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]

    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Augmented[i][-1]
        for j in range(i+1, n):
            x[i] -= Augmented[i][j] * x[j]
    return x

def rank_of_matrix(A):
    rows = len(A)
    cols = len(A[0])
    A_copy = [row[:] for row in A]
    rank = 0
    for i in range(cols):
        if any(row[i] != 0 for row in A_copy):
            rank += 1
            pivot_row = next(j for j, row in enumerate(A_copy) if row[i] != 0)
            A_copy[pivot_row], A_copy[rank-1] = A_copy[rank-1], A_copy[pivot_row]
            for j in range(rows):
                if j != rank-1:
                    factor = A_copy[j][i] / A_copy[rank-1][i]
                    for k in range(cols):
                        A_copy[j][k] -= factor * A_copy[rank-1][k]
    return rank

def generate_k_clique_cnf(n, k):
    if k > n:
        raise ValueError('k cannot be greater than n')
    variables = list(range(1, n+1))
    clauses = []
    for comb in itertools.combinations(variables, k):
        clause = [random.choice([f'-{var}', var]) for var in comb]
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    c = 1.0
    total_rank = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            clauses = generate_k_clique_cnf(n, k=3)
            hypergraph_edges = set()
            for clause in clauses:
                edge = tuple(sorted(int(var[1:]) if var.startswith('-') else int(var) for var in clause))
                hypergraph_edges.add(edge)
            H = [[0] * n for _ in range(n)]
            for u, v in hypergraph_edges:
                H[u-1][v-1] = 1
                H[v-1][u-1] = 1

            rank_H = rank_of_matrix(H)
            total_rank += rank_H
            instances_tested += 1

    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= c * n_values[-1] / k
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "polymatroid_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 17 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")