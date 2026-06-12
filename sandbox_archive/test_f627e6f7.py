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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [-v for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def clause_tree_width(clauses):
        if not clauses:
            return 0
        width = 0
        for clause in clauses:
            width = max(width, len([var for var in clause if var.startswith('x')]))
        return width
    
    def twisted_tensor_product(clauses):
        n = len(clauses[0])
        tensor = [[1] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for v in clause:
                if v.startswith('x'):
                    i = int(v[1:]) - 1
                    tensor[i][i+1] += 1
                    tensor[i+1][i] += 1
                else:
                    i = int(v[1:]) - 1
                    tensor[i][0] -= 1
                    tensor[0][i] -= 1
        return tensor
    
    def min_rank(tensor):
        n = len(tensor)
        rank = 0
        for _ in range(n):
            max_val = max(abs(val) for row in tensor if row != [0]*n)
            if max_val == 0:
                break
            rank += 1
            for i, row in enumerate(tensor):
                if abs(row[0]) == max_val:
                    pivot_row = row[:]
                    for j in range(n + 1):
                        tensor[i][j] /= max_val
                    for k in range(n):
                        if k != i and abs(tensor[k][0]) > 0:
                            factor = tensor[k][0]
                            for j in range(n + 1):
                                tensor[k][j] -= factor * pivot_row[j]
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        sum_yy = sum(yi ** 2 for yi in y)
        n = len(x)
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        if denominator == 0:
            return 0, 1.0
        correlation_coefficient = numerator / denominator
        r_squared = correlation_coefficient ** 2
        p_value = 1 - math.comb(n-2, 1) * r_squared / (1 - r_squared)
        return correlation_coefficient, p_value
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        clauses = generate_formula(n)
        ctw = clause_tree_width(clauses)
        tensor = twisted_tensor_product(clauses)
        mrt = min_rank(tensor)
        metric_values.append(ctw)
        metric_values.append(mrt)
    
    correlation_coefficient, p_value = pearson_correlation(metric_values[::2], metric_values[1::2])
    conjecture_holds = correlation_coefficient >= 0.5 and p_value <= 0.05
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")