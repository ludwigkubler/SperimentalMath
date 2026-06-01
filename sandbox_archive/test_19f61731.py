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
    
    def generate_sat_instance(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.randint(0, 1) else -random.choice(variables) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return variables, clauses
    
    def polynomial_to_matrix(poly, n):
        matrix = [[0] * n for _ in range(n)]
        for clause in poly:
            for var in clause:
                if var > 0:
                    row = var - 1
                else:
                    row = -var - 1
                matrix[row][abs(var) - 1] += 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def local_ring_norm(matrix):
        if not matrix:
            return 0
        det = 1
        n = len(matrix)
        for i in range(n):
            pivot_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                    pivot_row = j
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            det *= matrix[i][i]
        return abs(det) ** (1 / n)
    
    def clause_indicator_polynomial(clauses, n):
        poly = []
        for i in range(2**n):
            clause_eval = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    clause_eval[j] += 1
                else:
                    clause_eval[j] -= 1
            if all(x != 0 for x in clause_eval):
                poly.append(clause_eval)
        return poly
    
    def correlation_coefficient(norms, complexities):
        n = len(norms)
        mean_norm = sum(norms) / n
        mean_complexity = sum(complexities) / n
        numerator = sum((norms[i] - mean_norm) * (complexities[i] - mean_complexity) for i in range(n))
        denominator = math.sqrt(sum((norms[i] - mean_norm) ** 2 for i in range(n))) * math.sqrt(sum((complexities[i] - mean_complexity) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    def check_bound(norm, complexity):
        return norm <= 5 * math.sqrt(complexity)
    
    n_values = [5, 10, 15, 20, 30, 40]
    norms = []
    complexities = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            variables, clauses = generate_sat_instance(n, random.randint(1, n))
            poly = clause_indicator_polynomial(clauses, n)
            matrix = polynomial_to_matrix(poly, n)
            result = gaussian_elimination(matrix)
            if result is not None:
                norm = local_ring_norm(result)
                norms.append(norm)
                complexities.append(len(clauses))
                instances_tested += 1
                n_max = max(n_max, n)
    
    correlation = correlation_coefficient(norms, complexities)
    conjecture_holds = correlation > 0.8 and all(check_bound(norm, complexity) for norm, complexity in zip(norms, complexities))
    counterexample = "" if conjecture_holds else "correlation_too_low"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")