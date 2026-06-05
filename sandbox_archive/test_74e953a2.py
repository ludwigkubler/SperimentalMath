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
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def boolean_function_to_quaternion_matrix(cnf):
        n = len(cnf)
        matrix = [[0] * (2 * n) for _ in range(2 * n)]
        for i in range(n):
            a, b = cnf[i]
            matrix[a - 1][i] = 1
            matrix[b - 1][i + n] = 1
            matrix[i][a - 1] = 1
            matrix[i + n][b - 1] = 1
        return matrix
    
    def determinant(matrix):
        if len(matrix) == 0:
            return 1
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            sign = (-1) ** i
            det += sign * matrix[0][i] * determinant(submatrix)
        return det
    
    def min_order_quaternionic_k_theory(cnf):
        n = len(cnf)
        matrix = boolean_function_to_quaternion_matrix(cnf)
        det = determinant(matrix)
        return abs(det)
    
    def monotone_width(cnf):
        n = len(cnf)
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(clause[i] * clause[j] > 0 for clause in cnf):
                    width += 1
        return width
    
    results = []
    for s in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(s)
            min_order = min_order_quaternionic_k_theory(cnf)
            width = monotone_width(cnf)
            results.append((min_order, width))
    
    if not results:
        return {
            "metric_name": "min_order_K",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_width = sum(widths) / len(widths)
    
    conjecture_holds = all(1.5 * width <= min_order for min_order, width in zip(min_orders, widths))
    counterexample = "" if conjecture_holds else f"min_order={mean_min_order}, width={mean_width}"
    
    return {
        "metric_name": "min_order_K",
        "metric_value": mean_min_order,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")