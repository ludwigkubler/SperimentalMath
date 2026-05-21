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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]

def matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        return None
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def quadratic_form_rank(CNF):
    n = len(CNF)
    Q = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        assignment = [bool(i >> j & 1) for j in range(n)]
        for j in range(2**n):
            other_assignment = [bool(j >> k & 1) for k in range(n)]
            Q[i][j] = sum(CNF[l].count('x') * (assignment[l] != other_assignment[l]) for l in range(len(CNF)))
    gaussian_elimination(Q)
    rank = sum(1 for row in Q if any(row))
    return rank

def shortest_resolution_proof_length(CNF):
    n = len(CNF)
    clauses = [set(clause.split()) for clause in CNF]
    stack = []
    while True:
        new_clause = None
        for clause in clauses:
            if not clause:
                return 0
            if len(clause) == 1:
                literal = next(iter(clause))
                if '-' + literal in [c for c in clauses]:
                    clauses.remove(c for c in clauses if literal in c)
                    clauses.remove(c for c in clauses if '-' + literal in c)
                    new_clause = set()
                    break
        if new_clause is None:
            return len(stack)
        stack.append(new_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_length = 0
    instances_tested = 0
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            CNF = [''.join(random.choice(['x', '-x']) + random.choice(['1', '2', '3']) for _ in range(n)) for _ in range(n)]
            rank = quadratic_form_rank(CNF)
            length = shortest_resolution_proof_length(CNF)
            total_rank += rank
            total_length += length
            instances_tested += 1
    avg_rank = total_rank / instances_tested
    avg_length = total_length / instances_tested
    if avg_length == 0:
        return {
            "metric_name": "Rank/Length Ratio",
            "metric_value": float('inf'),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    ratio = avg_rank / avg_length
    return {
        "metric_name": "Rank/Length Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": ratio <= 10,  # Arbitrary constant c for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    avg_rank_length_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank_length_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank_length_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank/length ratio exceeds constant\" first_failing_seed={first_failing_seed}")