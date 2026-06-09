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

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_inverse(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        for j in range(k, n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def random_CNF(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(2, 3))]
        clauses.append(clause)
    return clauses

def eta_quotient_order(n):
    # This is a placeholder function. Implement the actual computation of the minimal order of an eta-quotient.
    return random.randint(1, n)

def frege_proof_width(CNF):
    # This is a placeholder function. Implement the actual computation of the Frege proof width.
    return len(CNF) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            CNF = random_CNF(n, n*2)
            eta_order = eta_quotient_order(n)
            proof_width = frege_proof_width(CNF)
            results.append((eta_order, proof_width))
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    eta_orders = [r[0] for r in results]
    proof_widths = [r[1] for r in results]
    n_max = max(len(eta_orders), len(proof_widths))
    mean_eta_order = sum(eta_orders) / len(eta_orders)
    mean_proof_width = sum(proof_widths) / len(proof_widths)
    covariance = sum((eta_orders[i] - mean_eta_order) * (proof_widths[i] - mean_proof_width) for i in range(len(eta_orders))) / len(eta_orders)
    variance_eta_order = sum((eta_orders[i] - mean_eta_order)**2 for i in range(len(eta_orders))) / len(eta_orders)
    variance_proof_width = sum((proof_widths[i] - mean_proof_width)**2 for i in range(len(proof_widths))) / len(proof_widths)
    pearson_corr = covariance / (math.sqrt(variance_eta_order) * math.sqrt(variance_proof_width))
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(pearson_corr) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")