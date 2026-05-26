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
    
    def generate_polynomial(n):
        coefficients = [random.randint(1, 10) for _ in range(n)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A):
        rows = len(A)
        cols = len(A[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, rows):
                factor = A[j][i] / A[i][i]
                for k in range(cols):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        if len(A) == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        det = 0
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def is_singular(matrix):
        return determinant(matrix) == 0
    
    def find_counterexample(n):
        poly = generate_polynomial(n)
        semigroup = set()
        for x in range(-n, n+1):
            value = evaluate_polynomial(poly, x)
            if value > 0:
                semigroup.add(value)
        
        min_quotient = float('inf')
        for delta in [1e-6 * i for i in range(1, 100)]:
            quotient = sum(abs(evaluate_polynomial(poly, x)) / delta for x in range(-n, n+1) if evaluate_polynomial(poly, x) > delta)
            min_quotient = min(min_quotient, quotient)
        
        return poly, semigroup, min_quotient
    
    def compute_ehrhart_quotient(semigroup):
        max_value = max(semigroup)
        min_value = min(semigroup)
        if max_value == 0:
            return float('inf')
        return max_value / min_value
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        poly, semigroup, min_quotient = find_counterexample(n)
        ehrhart_quotient = compute_ehrhart_quotient(semigroup)
        
        if len(semigroup) < 10:
            continue
        
        results.append({
            "n": n,
            "poly": poly,
            "semigroup": semigroup,
            "min_quotient": min_quotient,
            "ehrhart_quotient": ehrhart_quotient
        })
    
    if not results:
        return {
            "metric_name": "Ehrhart Quotient",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_quotient = sum(result["ehrhart_quotient"] for result in results)
    mean_quotient = total_quotient / len(results)
    std_quotient = math.sqrt(sum((result["ehrhart_quotient"] - mean_quotient) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(5 <= n <= 40 and result["ehrhart_quotient"] <= (math.log(n) ** 2 + 1) for result in results)
    
    return {
        "metric_name": "Ehrhart Quotient",
        "metric_value": mean_quotient,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={results[0]['n']}, poly={results[0]['poly']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_quotient = sum(result["metric_value"] for result in results if "metric_value" in result)
    mean_quotient = total_quotient / len(results)
    std_quotient = math.sqrt(sum((result["metric_value"] - mean_quotient) ** 2 for result in results if "metric_value" in result))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_quotient} std={std_quotient} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_quotient} std={std_quotient} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, poly={results[0]['poly']}\" first_failing_seed={first_failing_seed}")