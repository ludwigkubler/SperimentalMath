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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def calculate_sat_entropy(cnf):
        num_clauses = len(cnf)
        entropy = -num_clauses / math.log2(num_clauses)
        return entropy
    
    def calculate_quadratic_form(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        quadratic_form = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i, coeff in enumerate(clause):
                for j, coeff2 in enumerate(clause[i+1:], start=i+1):
                    quadratic_form[abs(coeff)][abs(coeff2)] += abs(coeff * coeff2)
        return quadratic_form
    
    def find_integral_points(quadratic_form):
        n = len(quadratic_form) - 1
        integral_points = []
        for x in range(-n, n + 1):
            for y in range(-n, n + 1):
                if all(quadratic_form[i][j] * (x**i * y**j) == 0 for i in range(n + 1) for j in range(n + 1)):
                    integral_points.append((x, y))
        return integral_points
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            for k in range(i+1, n):
                factor = Fraction(matrix[k][i], matrix[i][i])
                for j in range(n + 1):
                    matrix[k][j] -= factor * matrix[i][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(matrix[i][n], matrix[i][i])
            for k in range(i-1, -1, -1):
                matrix[k][n] -= matrix[k][i] * x[i]
        
        return x
    
    def calculate_min_integral_points(quadratic_form):
        n = len(quadratic_form) - 1
        integral_points = find_integral_points(quadratic_form)
        return len(integral_points)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        sat_entropy = calculate_sat_entropy(cnf)
        quadratic_form = calculate_quadratic_form(cnf)
        min_integral_points = calculate_min_integral_points(quadratic_form)
        results.append((min_integral_points, sat_entropy))
    
    if len(results) < 30:
        return {
            "metric_name": "MinIntegralPoints vs SATEntropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    min_integral_points = [x[0] for x, _ in results]
    sat_entropy = [x[1] for _, x in results]
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_dev_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / n)
        std_dev_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    corr_coeff = correlation_coefficient(min_integral_points, sat_entropy)
    
    return {
        "metric_name": "MinIntegralPoints vs SATEntropy",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": corr_coeff >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")