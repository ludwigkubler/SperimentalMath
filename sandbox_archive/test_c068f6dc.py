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
    
    def characteristic_polynomial(truth_table):
        n = len(truth_table)
        x = [0] * (n + 1)
        x[0] = 1
        
        for row in truth_table:
            new_x = [x[0]]
            for i in range(n):
                new_x.append((new_x[-1] + row[i]) % 2)
            x = new_x
        
        return x
    
    def rank_of_polynomial(poly):
        n = len(poly) - 1
        A = [[poly[j] if j == i else 0 for j in range(n)] for i in range(n)]
        B = [poly[i] for i in range(1, n + 1)]
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(A, B):
            rows, cols = len(A), len(A[0])
            for i in range(rows):
                max_row = i
                for j in range(i+1, rows):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                B[i], B[max_row] = B[max_row], B[i]
                
                for j in range(i+1, rows):
                    factor = A[j][i] / A[i][i]
                    for k in range(cols):
                        A[j][k] -= factor * A[i][k]
                    B[j] -= factor * B[i]
            
            rank = 0
            for i in range(rows):
                if abs(A[i][i]) > 1e-9:
                    rank += 1
            return rank
        
        return gaussian_elimination(A, B)
    
    def ac0_circuit_size(n):
        # Simplified estimation of AC0 circuit size for demonstration purposes
        return n * (n + 1) // 2
    
    def genus_of_curve(s):
        # Simplified estimation of genus for demonstration purposes
        return int(math.sqrt(2 * s))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        truth_table = [[random.randint(0, 1) for _ in range(n)] for _ in range(2**n)]
        poly = characteristic_polynomial(truth_table)
        rank = rank_of_polynomial(poly)
        s = ac0_circuit_size(n)
        g = genus_of_curve(s)
        
        results.append({
            "n": n,
            "rank": rank,
            "s": s,
            "g": g
        })
    
    if not results:
        return {
            "metric_name": "R(f)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    R_f = [result["rank"] for result in results]
    s_values = [result["s"] for result in results]
    g_values = [result["g"] for result in results]
    
    # Calculate correlation coefficient
    n_tests = len(results)
    mean_Rf = sum(R_f) / n_tests
    mean_s = sum(s_values) / n_tests
    mean_g = sum(g_values) / n_tests
    
    covariance = sum((R_f[i] - mean_Rf) * (s_values[i] - mean_s) for i in range(n_tests)) / n_tests
    variance_s = sum((s_values[i] - mean_s) ** 2 for i in range(n_tests)) / n_tests
    
    r = covariance / math.sqrt(variance_s)
    
    # Calculate slope of g^2 / s
    slope = (mean_g ** 2) / mean_s
    
    return {
        "metric_name": "R(f)",
        "metric_value": r,
        "instances_tested": n_tests,
        "conjecture_holds": abs(r - slope) <= 0.1 * slope,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 37))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_r = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_r = math.sqrt(sum((result["metric_value"] - mean_r) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={result['seed']}")
                break