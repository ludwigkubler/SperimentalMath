# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def communication_complexity(f):
        n = len(f)
        if n <= 1:
            return 0
        kappa_f = 0
        for x in range(2**(n-1)):
            y = f[x] ^ f[x + (1 << (n-1))]
            if y != f[x]:
                kappa_f += 1
        return kappa_f
    
    def symplectic_area(rho):
        n = len(rho)
        det_rho = determinant(rho)
        if det_rho == 0:
            return float('inf')
        return -2 * math.log(det_rho)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def generate_random_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def generate_random_density_matrix(n):
        rho = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            rho[i][i] = Fraction(1, 2)
        return rho
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        kappa_f_total = 0
        symplectic_area_total = 0
        instances_tested = 0
        
        for _ in range(50):
            f = generate_random_function(n)
            rho = generate_random_density_matrix(n)
            
            kappa_f = communication_complexity(f)
            area = symplectic_area(rho)
            
            kappa_f_total += kappa_f
            symplectic_area_total += area
            instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        mean_kappa_f = kappa_f_total / instances_tested
        mean_area = symplectic_area_total / instances_tested
        
        results.append({
            "n": n,
            "mean_kappa_f": mean_kappa_f,
            "mean_area": mean_area,
            "instances_tested": instances_tested
        })
    
    if not results:
        return {
            "metric_name": "symplectic_area",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "symplectic_area",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    kappa_f_values = [result["mean_kappa_f"] for result in results]
    area_values = [result["mean_area"] for result in results]
    
    def spearman_correlation(x, y):
        n = len(x)
        rank_x = {v: i+1 for i, v in enumerate(sorted(set(x), reverse=True))}
        rank_y = {v: i+1 for i, v in enumerate(sorted(set(y), reverse=True))}
        
        sum_diff_rank_squared = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        rho = 1 - (6 * sum_diff_rank_squared) / (n * (n**2 - 1))
        return rho
    
    rho = spearman_correlation(kappa_f_values, area_values)
    
    return {
        "metric_name": "symplectic_area",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": rho >= 0.7,
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
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho<{mean_rho}' first_failing_seed={first_failing_seed}")