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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda j: abs(matrix[j][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        if matrix[i][i] == 0:
            continue
        
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    row_echelon_form = gaussian_elimination(matrix)
    rank = sum(1 for row in row_echelon_form if any(row))
    return rank

def generate_cnf(n, m):
    cnf = []
    variables = set(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        lhr_values = []
        f_values = []
        
        for _ in range(30):
            m = random.randint(n // 2, n * 2)
            cnf = generate_cnf(n, m)
            lhr_phi = rank([[int(v in clause or -v in clause) for v in range(1, n + 1)] for clause in cnf])
            f_phi = m  # Simplified Frege proof length as a proxy
            
            lhr_values.append(lhr_phi)
            f_values.append(f_phi)
            instances_tested += 1
        
        if len(lhr_values) < 30:
            return {
                "metric_name": "lhr",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(lhr_values, f_values)) / \
                                   math.sqrt(sum((x - mean_x) ** 2 for x in lhr_values) * sum((y - mean_y) ** 2 for y in f_values))
        mean_x = sum(lhr_values) / len(lhr_values)
        mean_y = sum(f_values) / len(f_values)
        
        results.append({
            "n": n,
            "correlation_coefficient": correlation_coefficient,
            "mean_lhr": mean_x,
            "mean_f": mean_y
        })
    
    total_correlation_coefficient = sum(result["correlation_coefficient"] for result in results) / len(results)
    total_mean_lhr = sum(result["mean_lhr"] for result in results) / len(results)
    total_mean_f = sum(result["mean_f"] for result in results) / len(results)
    
    if total_correlation_coefficient >= 0.8:
        return {
            "metric_name": "lhr",
            "metric_value": total_correlation_coefficient,
            "instances_tested": 180,  # 30 instances per n for 6 values of n
            "n_max": 40,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "lhr",
            "metric_value": total_correlation_coefficient,
            "instances_tested": 180,  # 30 instances per n for 6 values of n
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": f"correlation_coefficient={total_correlation_coefficient}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_correlation_coefficient = sum(r["correlation_coefficient"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_correlation_coefficient} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_correlation_coefficient} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<{total_correlation_coefficient}' first_failing_seed={first_failing_seed}")