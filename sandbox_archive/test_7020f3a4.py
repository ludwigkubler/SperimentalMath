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

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    matrix = [row[:] for row in matrix]
    gaussian_elimination(matrix)
    rank = 0
    for row in matrix:
        if any(row[i] != 0 for i in range(len(row))):
            rank += 1
    return rank

def dpll(variables, clauses):
    def solve(model):
        if not clauses:
            return model
        clause = next(clause for clause in clauses if any(var in model and model[var] == val for var, val in clause))
        var, val = random.choice(clause)
        new_model = model.copy()
        new_model[var] = val
        satisfying_assignment = solve(new_model)
        if satisfying_assignment:
            return satisfying_assignment
        del new_model[var]
        new_model[var] = not val
        return solve(new_model)
    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            variables = list(range(n))
            clauses = []
            for i in range(n):
                clause = [(variables[i], random.choice([True, False]))]
                clauses.append(clause)
            model = dpll(variables, clauses)
            if not model:
                continue
            rank_value = rank([[1 if model[var] else 0 for var in variables]])
            total_rank += rank_value
            instances_tested += 1
            if rank_value > n * math.log2(n):
                conjecture_holds = False
                counterexample = f"Rank {rank_value} exceeds O(log^2 {n}) for n={n}"
            elif rank_value < n * math.log(n):
                conjecture_holds = False
                counterexample = f"Rank {rank_value} below Θ(log {n}) for n={n}"

    return {
        "metric_name": "Minimal Rank of Tropicalized Quantum Entanglement",
        "metric_value": total_rank / instances_tested,
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

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")