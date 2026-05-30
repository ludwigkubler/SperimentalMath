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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        complexity = float('inf')
        for x in range(2**(n-1)):
            y = f[x] ^ f[x + (1 << (n-1))]
            if y == 0:
                continue
            c = 0
            while y != 0:
                if y & 1:
                    c += 1
                y >>= 1
            complexity = min(complexity, c)
        return complexity
    
    def construct_density_matrix(f):
        n = len(f)
        rho = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for x in range(2**n):
            y = f[x] ^ f[x + (1 << (n-1))]
            if y == 0:
                continue
            p = Fraction(1, 2**(n-1))
            rho[x % n][x // n] += p
        return rho
    
    def symplectic_area(rho):
        n = len(rho)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(2 * (rho[i][j] - rho[j][i]))
        return area
    
    def generate_random_density_matrix(n):
        rho = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            rho[i][i] = Fraction(1)
        return rho
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        kappa_f = communication_complexity(f)
        rho = construct_density_matrix(f)
        area = symplectic_area(rho)
        
        if kappa_f == float('inf'):
            continue
        
        results.append({
            "n": n,
            "kappa_f": kappa_f,
            "area": area
        })
    
    if not results:
        return {
            "metric_name": "symplectic_area",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    kappa_f_values = [r["kappa_f"] for r in results]
    area_values = [r["area"] for r in results]
    
    def rank_correlation(x, y):
        n = len(x)
        x_rank = {x[i]: i+1 for i in range(n)}
        y_rank = {y[i]: i+1 for i in range(n)}
        
        sum_diff_squares = 0
        for i in range(n):
            sum_diff_squares += (x_rank[x[i]] - y_rank[y[i]]) ** 2
        
        rho = 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
        return rho
    
    rho = rank_correlation(kappa_f_values, area_values)
    
    return {
        "metric_name": "symplectic_area",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": rho >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all(r["conjecture_holds"] for r in results):
        counterexample = [r for r in results if not r["conjecture_holds"]]
        first_failing_seed = counterexample[0]["seed"]
        RESULT = f"RESULT: FALSIFIED counterexample=\"rho < 0.7\" first_failing_seed={first_failing_seed}"
    else:
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}"
    
    print(RESULT)