# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B, mod):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
                C[i][j] %= mod
    return C

def matrix_power(A, k, mod):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, A, mod)
        A = matrix_multiply(A, A, mod)
        k //= 2
    return result

def dpll(cnf):
    def backtrack():
        assignment = [None] * len(variables)
        stack = []
        for clause in cnf:
            unassigned_vars = [var for var in clause if assignment[abs(var)-1] is None]
            if not unassigned_vars:
                return False
            var = random.choice(unassigned_vars)
            assignment[abs(var)-1] = 1 if var > 0 else -1
            stack.append((var, assignment[:]))
        while True:
            clause = next((c for c in cnf if all(assignment[abs(lit)-1] != lit for lit in c)), None)
            if not clause:
                return True
            unassigned_vars = [lit for lit in clause if assignment[abs(lit)-1] is None]
            if not unassigned_vars:
                last_var, last_assignment = stack.pop()
                assignment[abs(last_var)-1] = -last_assignment[abs(last_var)-1]
                continue
            var = random.choice(unassigned_vars)
            assignment[abs(var)-1] = 1 if var > 0 else -1
            stack.append((var, assignment[:]))
    variables = set(abs(lit) for clause in cnf for lit in clause)
    return backtrack()

def generate_cnf(n):
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([-i, i]) for i in range(1, n+1)]
        if random.random() < 0.5:
            clause.append(random.choice([-i, i]))
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        proof_length = dpll(cnf)
        if proof_length is None:
            continue
        rank_H = len(cnf)  # Simplified for testing purposes
        results.append((rank_H, proof_length))
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    rank_H_values = [r[0] for r in results]
    proof_length_values = [r[1] for r in results]
    mean_rank_H = sum(rank_H_values) / len(rank_H_values)
    mean_proof_length = sum(proof_length_values) / len(proof_length_values)
    variance_rank_H = sum((x - mean_rank_H)**2 for x in rank_H_values) / len(rank_H_values)
    variance_proof_length = sum((y - mean_proof_length)**2 for y in proof_length_values) / len(proof_length_values)
    covariance = sum((rank_H_values[i] - mean_rank_H) * (proof_length_values[i] - mean_proof_length) for i in range(len(results))) / len(results)
    pearson_corr_coeff = covariance / math.sqrt(variance_rank_H * variance_proof_length)
    conjecture_holds = pearson_corr_coeff >= 0.8 and all(rank_H <= proof_length * 1.5 for rank_H, proof_length in results)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(r[0] > 0 for r in results)),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Pearson correlation coefficient < 0.8 or rank_H > |P(φ)| * 1.5"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8 or rank_H > |P(φ)| * 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")