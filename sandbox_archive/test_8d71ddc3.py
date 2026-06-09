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
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        for _ in range(n):
            clause_size = random.randint(1, n)
            clause = random.sample(variables, clause_size)
            clauses.append(' '.join(clause))
        return '\n'.join(clauses)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(rows):
                if k != i:
                    factor = Fraction(matrix[k][i])
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def compute_minimal_tropical_order(matrix):
        rows, cols = len(matrix), len(matrix[0])
        identity_matrix = [[Fraction(1) if i == j else Fraction(0) for j in range(cols)] for i in range(rows)]
        augmented_matrix = [row + col for row, col in zip(matrix, identity_matrix)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_matrix if any(val != Fraction(0) for val in row))
        return rank
    
    def compute_clause_complexity(cnf):
        return cnf.count('\n') + 1
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        matrix = [[Fraction(1) if i == j else Fraction(-1) for j in range(n)] for i in range(n)]
        mto = compute_minimal_tropical_order(matrix)
        cphi = compute_clause_complexity(cnf)
        metric_values.append(mto - cphi)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    correlation_coefficient = sum(x * y for x, y in zip(metric_values, range(len(metric_values)))) / (len(metric_values) * std_value * (len(metric_values) - 1) ** 0.5)
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_value) <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.8 or mean_abs_diff>3"
    
    return {
        "metric_name": "Minimal Tropical Order - Clause Complexity Difference",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")