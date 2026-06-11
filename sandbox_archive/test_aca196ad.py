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
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * (matrix[1][1] - matrix[1][2]) % mod
    det %= mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[(matrix[(i+1) % n][(j+1) % n] - matrix[(i+1) % n][(j+2) % n]) * (matrix[0][0] if i == 0 and j == 0 else matrix[0][1] if i == 0 and j == 1 else matrix[0][2]) for j in range(n)] for i in range(n)]
    inv_matrix = [[(inv_det * adjugate[i][j]) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_exp(matrix, exp, mod):
    result = [[0 if i != j else 1 for j in range(len(matrix))] for i in range(len(matrix))]
    base = matrix
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult(result, base)
        base = matrix_mult(base, base)
        exp //= 2
    return [[(result[i][j] + mod) % mod for j in range(len(matrix))] for i in range(len(matrix))]

def quasi_morphism_entanglement(formula):
    n = len(formula)
    entanglement_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if formula[i][j]:
                entanglement_matrix[i][j] = 1
                entanglement_matrix[j][i] = 1
    identity_matrix = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    entanglement_exp = matrix_exp(entanglement_matrix, n-1, n)
    return sum(sum(row) for row in entanglement_exp) / (n * (n - 1))

def clause_satisfiability_complexity(formula):
    n = len(formula)
    max_clauses = 0
    for i in range(n):
        for j in range(i+1, n):
            if formula[i][j]:
                max_clauses += 1
    return max_clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    trials = [5, 10, 15, 20, 30, 40]
    results = []
    for n in trials:
        formula = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        o_qm = quasi_morphism_entanglement(formula)
        c_s = clause_satisfiability_complexity(formula)
        results.append((o_qm, c_s))
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    o_qm_values = [result[0] for result in results]
    c_s_values = [result[1] for result in results]
    n_max = max(trials)
    correlation_coefficient = sum((o_qm_values[i] - mean_o_qm) * (c_s_values[i] - mean_c_s) for i in range(len(results))) / (len(results) * std_o_qm * std_c_s)
    mean_o_qm = sum(o_qm_values) / len(o_qm_values)
    mean_c_s = sum(c_s_values) / len(c_s_values)
    std_o_qm = math.sqrt(sum((x - mean_o_qm) ** 2 for x in o_qm_values) / len(o_qm_values))
    std_c_s = math.sqrt(sum((x - mean_c_s) ** 2 for x in c_s_values) / len(c_s_values))
    if correlation_coefficient > 0.8:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std={math.sqrt(sum((result['metric_value'] - (sum(result['metric_value'] for result in results) / len(results))) ** 2 for result in results) / len(results))} support_fraction={support_fraction}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")