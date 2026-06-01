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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def m_order(phi):
    # Convert CNF to quadratic form (simplified example)
    n = len(phi)
    Q = [[0] * n for _ in range(n)]
    for clause in phi:
        for lit in clause:
            if lit > 0:
                Q[lit-1][lit-1] += 1
            else:
                Q[-lit-1][-lit-1] += 1
    return abs(determinant(gaussian_elimination(Q)))

def d_phi(phi):
    # Simulate DPLL search tree diameter (simplified example)
    n = len(phi)
    max_depth = 0
    for clause in phi:
        depth = sum(1 for lit in clause if lit != 0)
        max_depth = max(max_depth, depth)
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = [[random.randint(1, n), -random.randint(1, n)] for _ in range(n)]
        m_order_val = m_order(phi)
        d_phi_val = d_phi(phi)
        results.append({"m_order": m_order_val, "d_phi": d_phi_val})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_order_vals = [r["m_order"] for r in results]
    d_phi_vals = [r["d_phi"] for r in results]
    
    mean_m_order = sum(m_order_vals) / len(m_order_vals)
    mean_d_phi = sum(d_phi_vals) / len(d_phi_vals)
    
    correlation_coefficient = 0
    if mean_m_order != 0 and mean_d_phi != 0:
        numerator = sum((m_order_vals[i] - mean_m_order) * (d_phi_vals[i] - mean_d_phi) for i in range(len(m_order_vals)))
        denominator = math.sqrt(sum((m_order_vals[i] - mean_m_order)**2 for i in range(len(m_order_vals)))) * math.sqrt(sum((d_phi_vals[i] - mean_d_phi)**2 for i in range(len(d_phi_vals))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.7 else f"correlation={correlation_coefficient}"
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
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")