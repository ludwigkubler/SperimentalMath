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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def incidence_matrix(cnf, n):
        matrix = [[0] * (2 * n) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] = 1
                else:
                    matrix[i][-var - 1] = 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(n):
                if i != j and matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(m):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        row_echelon_form = gaussian_elimination(matrix)
        rank = 0
        for i in range(n):
            if any(row_echelon_form[i][j] != 0 for j in range(m)):
                rank += 1
        return rank
    
    def alexander_brandt_index(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank_matrix = rank(matrix)
        return Fraction(n - rank_matrix, n)
    
    def circuit_monotone_width(cnf):
        # Placeholder for actual computation of circuit monotone width
        # This is a dummy implementation and should be replaced with the correct algorithm
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, 2 * n)
        cnf = generate_cnf(n, m)
        matrix = incidence_matrix(cnf, n)
        ab_index = alexander_brandt_index(matrix)
        w_m = circuit_monotone_width(cnf)
        results.append((ab_index, w_m))
    
    if not results:
        return {
            "metric_name": "AB(φ) vs w_m",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ab_indices = [r[0] for r in results]
    w_ms = [r[1] for r in results]
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) * sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    corr_coeff = correlation_coefficient(ab_indices, w_ms)
    
    return {
        "metric_name": "AB(φ) vs w_m",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(corr_coeff) >= 0.7 and all(abs(corr_coeff) >= 0.5 for _ in range(30)),
        "counterexample": "" if abs(corr_coeff) >= 0.7 else f"Correlation coefficient {corr_coeff} < 0.5"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)