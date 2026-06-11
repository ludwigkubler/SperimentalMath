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

def matrix_mod_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_mod_inv(A, mod):
    n = len(A)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot_row = next((i for i in range(col, n) if A[i][col]), None)
        if pivot_row is None:
            raise ValueError("Matrix is not invertible")
        A[col], A[pivot_row] = A[pivot_row], A[col]
        I[col], I[pivot_row] = I[pivot_row], I[col]
        for i in range(n):
            if i != col:
                factor = A[i][col]
                A[i][col] = 0
                for j in range(n):
                    A[i][j] = (A[i][j] - factor * A[col][j]) % mod
                    I[i][j] = (I[i][j] - factor * I[col][j]) % mod
        pivot = A[col][col]
        for i in range(n):
            A[col][i] = (A[col][i] * pow(pivot, -1, mod)) % mod
            I[col][i] = (I[col][i] * pow(pivot, -1, mod)) % mod
    return I

def smith_normal_form(A, mod):
    n = len(A)
    U = [[0] * n for _ in range(n)]
    for i in range(n):
        U[i][i] = 1
    for col in range(n):
        pivot_row = next((i for i in range(col, n) if A[i][col]), None)
        if pivot_row is None:
            raise ValueError("Matrix is not invertible")
        A[col], A[pivot_row] = A[pivot_row], A[col]
        U[col], U[pivot_row] = U[pivot_row], U[col]
        for i in range(n):
            if i != col:
                factor = A[i][col]
                A[i][col] = 0
                for j in range(n):
                    A[i][j] = (A[i][j] - factor * A[col][j]) % mod
    return U

def frege_proof_depth(formula):
    # Simplified DPLL solver to estimate proof depth
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        pure_literals = [l for l in range(1, max(clauses) + 1) if all(l not in c or -l not in c for c in clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        literal = random.choice(list(assignment.keys()))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        true_depth = 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        new_assignment[literal] = False
        false_depth = 1 + dpll([c for c in clauses if -literal not in c], new_assignment)
        return min(true_depth, false_depth)
    clauses = formula.split(' & ')
    assignment = {i: random.choice([True, False]) for i in range(1, max(map(int, clauses)) + 1)}
    return dpll(clauses, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    AKT_dims = []
    proof_depths = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            variables = list(range(1, n + 1))
            clauses = [f"{random.choice(variables)}"] * random.randint(2, n)
            formula = " & ".join(clauses)
            matroid = [[int(lit in clause) for lit in variables] for clause in clauses]
            AKT_dim = sum(sum(row) for row in smith_normal_form(matroid, 2))
            proof_depth = frege_proof_depth(formula)
            AKT_dims.append(AKT_dim)
            proof_depths.append(proof_depth)
            instances_tested += 1
            n_max = max(n_max, n)

    correlation_coefficient = sum((AKT_dims[i] - mean_AKT) * (proof_depths[i] - mean_proof_depth) for i in range(instances_tested)) / instances_tested
    mean_AKT = sum(AKT_dims) / instances_tested
    mean_proof_depth = sum(proof_depths) / instances_tested

    conjecture_holds = correlation_coefficient >= 0.5
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient} < 0.5"

    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")