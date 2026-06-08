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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    M[i][j] = 1
        return M
    
    def frobenius_schur_index(M):
        n = len(M)
        trace = sum(M[i][i] for i in range(n))
        det = determinant(M, n)
        return abs(trace / det) if det != 0 else float('inf')
    
    def determinant(M, n):
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += ((-1) ** j) * M[0][j] * determinant(submatrix, n - 1)
        return det
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_communication = 0
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    comm = bin(i ^ j).count('1')
                    if comm > max_communication:
                        max_communication = comm
        return max_communication
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        return cov / (std_x * std_y)
    
    def check_fsi_bound(fsi_min):
        return fsi_min <= 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    fsi_min_values = []
    cc_lower_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = matrix_representation(f)
        fsi_min = frobenius_schur_index(M)
        cc_lower = communication_complexity(f)
        
        if fsi_min == float('inf'):
            return {
                "metric_name": "FSI_min",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        fsi_min_values.append(fsi_min)
        cc_lower_values.append(cc_lower)
    
    if not check_fsi_bound(max(fsi_min_values)):
        return {
            "metric_name": "FSI_min",
            "metric_value": max(fsi_min_values),
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"FSI_min > 10 for n={max(n_values)}"
        }
    
    slope, intercept = linear_regression(fsi_min_values, cc_lower_values)
    corr_coeff = correlation_coefficient(fsi_min_values, cc_lower_values)
    
    return {
        "metric_name": "FSI_min",
        "metric_value": corr_coeff,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"FSI_min > 10\" first_failing_seed={first_failing_seed}")