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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def matrix_multiplication(A, B):
        m = len(A)
        k = len(B[0])
        result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for r in range(n):
                if r != i:
                    factor = augmented_matrix[r][i]
                    for j in range(n + 1):
                        augmented_matrix[r][j] -= factor * augmented_matrix[i][j]
        return [row[:-1] for row in augmented_matrix]
    
    def frobenius_schur_indicator(matrix):
        n = len(matrix)
        det = 0
        for perm in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j for i, j in zip(perm, range(n)))
            product = math.prod(matrix[i][j] for i, j in enumerate(perm))
            det += sign * product
        return abs(det)
    
    def resolution_width(cnf):
        stack = []
        for clause in cnf:
            if any(var in stack for var in clause):
                continue
            stack.append(random.choice(clause))
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    indicators = []
    widths = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            matrix = [[random.randint(-1, 1) for _ in range(n)] for _ in range(n)]
            indicator = frobenius_schur_indicator(matrix)
            width = resolution_width(cnf)
            indicators.append(indicator)
            widths.append(width)
            instances_tested += 1
    
    if not indicators or not widths:
        return {
            "metric_name": "Frobenius-Schur Indicator vs Resolution Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((indicators[i] - mean_ind) * (widths[i] - mean_width) for i in range(len(indicators))) / len(indicators)
    mean_diff = abs(sum(indicators[i] - widths[i] for i in range(len(indicators)))) / len(indicators)
    mean_ind = sum(indicators) / len(indicators)
    mean_width = sum(widths) / len(widths)
    
    return {
        "metric_name": "Frobenius-Schur Indicator vs Resolution Width",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 3,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")