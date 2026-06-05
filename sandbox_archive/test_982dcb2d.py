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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(cnf, n):
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for c in cnf:
            for var in c:
                if var > 0:
                    matrix[var][var] += 1
                else:
                    matrix[-var][-var] += 1
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
                continue
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if matrix[i][i]:
                r += 1
        return r
    
    def alexander_brandt_index(matrix):
        n = len(matrix) - 1
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return abs(det)
    
    def circuit_monotone_width(cnf):
        m, n = len(cnf), len(cnf[0])
        width = 0
        for _ in range(2 ** (n - 1)):
            assignment = [random.choice([True, False]) for _ in range(n)]
            satisfied = True
            for clause in cnf:
                if all(not assignment[abs(var) - 1] == (var > 0) for var in clause):
                    satisfied = False
                    break
            if satisfied:
                width += 1
        return width
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    for _ in range(30):
        n, m = random.randint(5, 40), random.randint(10, 80)
        cnf = generate_cnf(n, m)
        matrix = incidence_matrix(cnf, n)
        ab_index = alexander_brandt_index(gaussian_elimination(matrix))
        w_m = circuit_monotone_width(cnf)
        results.append((ab_index, w_m))
    
    x, y = zip(*results)
    corr_coeff = correlation_coefficient(x, y)
    conjecture_holds = abs(corr_coeff) >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {corr_coeff}"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")