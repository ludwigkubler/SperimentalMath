# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def matrix_mult(A, B, mod):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
                    C[i][j] %= mod
        return C
    
    def matrix_exp(M, k, mod):
        result = [[Fraction(1) if i == j else Fraction(0) for j in range(len(M))] for i in range(len(M))]
        while k > 0:
            if k % 2 == 1:
                result = matrix_mult(result, M, mod)
            M = matrix_mult(M, M, mod)
            k //= 2
        return result
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        poly = [identity]
        for i in range(1, n + 1):
            new_poly = matrix_mult(matrix, poly[-1], n)
            poly.append(new_poly)
        return poly
    
    def determinant(poly):
        n = len(poly)
        det = Fraction(0)
        for i in range(n):
            term = (-1) ** i * poly[i][i]
            submatrix = [row[:i] + row[i+1:] for row in poly[1:]]
            det += term * determinant(submatrix)
        return det
    
    def geometric_complexity_group_size(cnf):
        n = len(cnf)
        mod = 2 ** (n + 1) - 1
        A = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                A[abs(lit) - 1][n] += Fraction(1)
                A[n][abs(lit) - 1] -= Fraction(1)
        A = matrix_exp(A, n, mod)
        det = determinant(A)
        return abs(det)
    
    def resolution_proof_width(cnf):
        n = len(cnf)
        width = 0
        for clause in cnf:
            width = max(width, len(clause))
        return width
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            gcs = geometric_complexity_group_size(cnf)
            rpw = resolution_proof_width(cnf)
            results.append((gcs, rpw))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    gcs_values = [gcs for gcs, _ in results]
    rpw_values = [rpw for _, rpw in results]
    
    mean_gcs = sum(gcs_values) / len(gcs_values)
    mean_rpw = sum(rpw_values) / len(rpw_values)
    
    covariance = sum((gcs - mean_gcs) * (rpw - mean_rpw) for gcs, rpw in results) / len(results)
    variance_gcs = sum((gcs - mean_gcs) ** 2 for gcs in gcs_values) / len(gcs_values)
    variance_rpw = sum((rpw - mean_rpw) ** 2 for rpw in rpw_values) / len(rpw_values)
    
    pearson_corr = covariance / (variance_gcs * variance_rpw) ** 0.5
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in [results[i][1] for i in range(len(results))]),
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": "" if pearson_corr >= 0.5 else f"pearson_corr={pearson_corr}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and "counterexample" in result and result["counterexample"].startswith("pearson_corr=") for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and "counterexample" in result and result["counterexample"].startswith("pearson_corr="))
        pearson_corr = float(result["counterexample"][13:])
        print(f"RESULT: FALSIFIED counterexample='pearson_corr={pearson_corr}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")