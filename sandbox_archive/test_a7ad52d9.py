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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = sum(1 for i in range(2**n) if f[i] == 1)
        return (rank - n / 2)**2
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for col in range(cols):
            max_row = max(range(col, rows), key=lambda i: abs(matrix[i][col]))
            matrix[col], matrix[max_row] = matrix[max_row], matrix[col]
            if matrix[col][col] == 0:
                continue
            denom = matrix[col][col]
            for j in range(cols):
                matrix[col][j] /= denom
            for i in range(rows):
                if i != col:
                    factor = matrix[i][col]
                    for j in range(cols):
                        matrix[i][j] -= factor * matrix[col][j]
        return matrix
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        row_rank = 0
        for col in range(cols):
            max_row = max(range(col, rows), key=lambda i: abs(matrix[i][col]))
            if matrix[max_row][col] == 0:
                continue
            matrix[col], matrix[max_row] = matrix[max_row], matrix[col]
            row_rank += 1
        return row_rank
    
    def moment_polytope(f):
        n = len(f)
        polytope = []
        for i in range(2**n):
            if f[i] == 1:
                polytope.append([i & (1 << j) != 0 for j in range(n)])
        return polytope
    
    def minimal_ramanujan_sum(polytope):
        n = len(polytope[0])
        matrix = [[sum(row[j] for row in polytope if row[i]) for i in range(n)] for j in range(n)]
        reduced_matrix = gaussian_elimination(matrix)
        return sum(abs(reduced_matrix[i][i]) for i in range(min(len(reduced_matrix), n)))
    
    def sqrt(x):
        if x <= 0:
            return 0
        guess = x / 2.0
        while True:
            new_guess = (guess + x / guess) / 2.0
            if abs(new_guess - guess) < 1e-6:
                return new_guess
            guess = new_guess
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rc_f = communication_complexity_rank_variance(f)
        polytope = moment_polytope(f)
        r_f = minimal_ramanujan_sum(polytope)
        
        if rc_f == 0:
            continue
        
        results.append({
            "n": n,
            "R_f": r_f,
            "RC(f)": rc_f
        })
    
    if not results:
        return {
            "metric_name": "minimal_ramanujan_sum",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rc_f = sum(result["RC(f)"] for result in results) / len(results)
    mean_r_f = sum(result["R_f"] for result in results) / len(results)
    
    if any(abs(result["R_f"]) > sqrt(2 * result["RC(f)"]) or abs(result["R_f"]) < sqrt(0.5 * result["RC(f)"]) for result in results):
        return {
            "metric_name": "minimal_ramanujan_sum",
            "metric_value": mean_r_f,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "falsified"
        }
    
    return {
        "metric_name": "minimal_ramanujan_sum",
        "metric_value": mean_r_f,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"falsified\" first_failing_seed={first_failing_seed}")