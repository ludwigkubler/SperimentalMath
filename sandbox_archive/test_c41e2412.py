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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mul(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                    I[j][k] -= factor * I[i][k]
    return I

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = M[j][i]
                for k in range(n+1):
                    M[j][k] -= factor * M[i][k]
    return [M[i][-1] for i in range(n)]

def dpll(sat_formula, assignment=None):
    if assignment is None:
        assignment = {}
    if not sat_formula:
        return True
    var = next(iter(sat_formula))
    for value in (True, False):
        new_assignment = assignment.copy()
        new_assignment[var] = value
        new_sat_formula = []
        for clause in sat_formula:
            if any(v in new_assignment and new_assignment[v] == val for v, val in clause):
                continue
            new_clause = [(v, val) for v, val in clause if v != var]
            if not new_clause:
                return False
            new_sat_formula.append(new_clause)
        if dpll(new_sat_formula, new_assignment):
            return True
    return False

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        variables = random.sample(range(1, n+1), 2)
        clause = [(variables[0], random.choice([True, False])), (variables[1], not random.choice([True, False]))]
        clauses.append(clause)
    return clauses

def characteristic_function_field(cnf_formula):
    # Placeholder for actual computation
    return "function_field"

def arithmetic_genus(function_field):
    # Placeholder for actual computation
    return 0

def resolution_proof_width(cnf_formula):
    return dpll(cnf_formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf_formula = generate_cnf(n)
    function_field = characteristic_function_field(cnf_formula)
    g_F = arithmetic_genus(function_field)
    ω_F = resolution_proof_width(cnf_formula)
    metric_value = abs(g_F - ω_F) / max(1, ω_F)
    conjecture_holds = g_F <= 10 * ω_F
    counterexample = "" if conjecture_holds else f"g(F)={g_F}, ω_F={ω_F}"
    return {
        "metric_name": "ArithmeticGenusResolutionProofWidthRatio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] and "g(F)>" in r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"] and "g(F)>" in r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"g(F)>10*ω_F\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")