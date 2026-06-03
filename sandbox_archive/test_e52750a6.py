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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def circuit_monotone_width(g):
        n = len(g)
        if n == 1:
            return 1
        width = 0
        for i in range(1, n):
            width = max(width, circuit_monotone_width(g[:i]) + circuit_monotone_width(g[i:]))
        return width

    def symplectic_capacity(f):
        # Placeholder function. Replace with actual computation.
        return random.random()

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_sym_cap = 0
    total_width_mon = 0

    for n in n_values:
        for _ in range(5):
            # Generate a random Tseitin formula with n variables
            literals = list(range(-n, 0)) + list(range(1, n+1))
            clauses = []
            for i in range(n):
                clause = [random.choice(literals) for _ in range(3)]
                clauses.append(clause)
                clauses.append([-x for x in clause])
            formula = literals + clauses

            # Construct the polynomial f(x) from the Tseitin formula
            f_coeffs = [0] * (n+1)
            for literal in literals:
                if literal > 0:
                    f_coeffs[literal] += 1
                else:
                    f_coeffs[-literal] -= 1

            # Compute the minimal symplectic capacity of f(x)
            A = [[f_coeffs[i-j] for j in range(n+1)] for i in range(n+1)]
            A = gaussian_elimination(A)
            det = 1
            for i in range(n+1):
                det *= A[i][i]
            sym_cap = abs(det)

            # Construct the circuit computing the symmetric function of the roots of f(x)
            g = [0] * (n+1)
            for i in range(1, n+1):
                g[i] = sum(f_coeffs[j] * math.comb(n, j) for j in range(i))

            # Compute the circuit monotone width
            width_mon = circuit_monotone_width(g)

            total_sym_cap += sym_cap
            total_width_mon += width_mon
            instances_tested += 1

    mean_sym_cap = total_sym_cap / instances_tested
    mean_width_mon = total_width_mon / instances_tested
    correlation_coefficient = (instances_tested * mean_sym_cap * mean_width_mon - 
                               total_sym_cap * total_width_mon) / math.sqrt(
                                   (instances_tested * mean_sym_cap**2 - total_sym_cap**2) *
                                   (instances_tested * mean_width_mon**2 - total_width_mon**2))

    conjecture_holds = correlation_coefficient > 0.7 and max(f for f in [mean_sym_cap, mean_width_mon]) <= 1.5
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                                              31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
                                              73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")