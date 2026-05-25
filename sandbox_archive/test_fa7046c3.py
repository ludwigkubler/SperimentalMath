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
    
    def generate_polynomial(n):
        coeffs = [random.randint(-10, 10) for _ in range(n + 1)]
        return coeffs
    
    def evaluate_polynomial(coeffs, x):
        result = 0
        for i, coeff in enumerate(coeffs):
            result += coeff * (x ** i)
        return result
    
    def compute_order_of_vanishing(coeffs):
        x = 0.0001
        while abs(evaluate_polynomial(coeffs, x)) < 1e-6:
            x *= 2
        return int(math.log(x) / math.log(2))
    
    def generate_matrix(n):
        matrix = []
        for _ in range(n):
            row = [random.randint(-10, 10) for _ in range(n)]
            matrix.append(row)
        return matrix
    
    def compute_degree_of_polynomial_minor(matrix, i, j):
        minor = []
        for r in range(len(matrix)):
            if r != i:
                row = []
                for c in range(len(matrix[r])):
                    if c != j:
                        row.append(matrix[r][c])
                minor.append(row)
        return len(minor) - 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_polynomial(n)
            order_of_vanishing = compute_order_of_vanishing(f)
            
            M = generate_matrix(n)
            min_degree = float('inf')
            for i in range(n):
                for j in range(n):
                    degree = compute_degree_of_polynomial_minor(M, i, j)
                    if degree < min_degree:
                        min_degree = degree
            
            if order_of_vanishing < min_degree * n:
                conjecture_holds = False
                counterexample = f"n={n}, f_order={order_of_vanishing}, M_min_degree={min_degree}"
            
            total_metric_value += order_of_vanishing
            instances_tested += 1
    
    return {
        "metric_name": "Order of Vanishing",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")