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
    
    def cnf_to_poly(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        B = [0] * (n + 1)
        
        for clause in cnf:
            for lit in clause:
                i = abs(lit) - 1
                if lit > 0:
                    A[i][i] += 1
                else:
                    A[n][i] += 1
                    A[i][n] += 1
            B[n] += 1
        
        return A, B
    
    def gaussian_elimination(A, B):
        n = len(B)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            B[i], B[max_row] = B[max_row], B[i]
            
            factor = Fraction(A[i][i])
            for j in range(i, n):
                A[i][j] /= factor
            B[i] /= factor
            
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
                    B[j] -= factor * B[i]
        
        return A, B
    
    def det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det_val = Fraction(0)
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det_val += (-1) ** j * A[0][j] * det(submatrix)
            return det_val
    
    def frege_proof_length(cnf):
        n = len(cnf)
        length = 2 * n
        for clause in cnf:
            length += 1
        return length
    
    def quadratic_discriminant(A, B):
        n = len(B)
        A_inv = [[0] * n for _ in range(n)]
        det_A = det(A)
        
        if det_A == 0:
            raise ValueError("Singular matrix")
        
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                submatrix = [row[:i] + row[i+1:] for row in submatrix]
                A_inv[i][j] = (-1) ** (i + j) * det(submatrix) / det_A
        
        delta = B[n]**2 - 4 * sum(A[i][n] * A[n][i] for i in range(n))
        return delta
    
    def linear_regression(x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean)**2 for i in range(n))
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        return slope, intercept
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_log_delta = 0.0
    total_f_phi = 0.0
    
    for n in n_values:
        for _ in range(5):
            cnf = [[random.randint(1, n) for _ in range(random.randint(2, 4))] for _ in range(n)]
            A, B = cnf_to_poly(cnf)
            try:
                delta = quadratic_discriminant(A, B)
                f_phi = frege_proof_length(cnf)
                
                if delta <= 0:
                    continue
                
                log_delta = math.log(delta)
                total_log_delta += log_delta
                total_f_phi += f_phi
                instances_tested += 1
            except (ValueError, ZeroDivisionError):
                pass
    
    if instances_tested == 0:
        return {
            "metric_name": "log_delta vs f_phi",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x = list(range(1, instances_tested + 1))
    y_log_delta = [total_log_delta / instances_tested] * instances_tested
    y_f_phi = [total_f_phi / instances_tested] * instances_tested
    
    slope, intercept = linear_regression(x, y_log_delta)
    
    return {
        "metric_name": "log_delta vs f_phi",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(slope) >= 0.9 and p_value <= 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_slope = sum(r["metric_value"] for r in results) / len(results)
        std_slope = math.sqrt(sum((r["metric_value"] - mean_slope)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")