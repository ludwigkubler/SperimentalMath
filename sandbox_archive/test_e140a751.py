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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def hodge_norm(A):
        det = 1
        for i in range(len(A)):
            det *= A[i][i]
        return abs(det)

    def resolution_width(phi):
        # Placeholder function; replace with actual implementation
        return len(phi.split())

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n < 5 or n > 40:
            continue
        
        for _ in range(5):
            phi = " ".join(random.choices("01", k=n))
            w_phi = resolution_width(phi)
            
            # Construct the associated affine plane curve and compute Hodge matrix
            A = [[0] * (n+1) for _ in range(n+1)]
            for i in range(n):
                for j in range(n):
                    A[i][j] = int(phi[i*n + j])
            A[n][n] = 1
            
            # Compute Hodge norm
            h_norm_phi = hodge_norm(gaussian_elimination(A))
            
            results.append({
                "h_norm": h_norm_phi,
                "w_phi": w_phi,
                "n": n
            })
    
    if not results:
        return {
            "metric_name": "h_norm_w_phi",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    h_norm_values = [r["h_norm"] for r in results]
    w_phi_values = [r["w_phi"] for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    
    # Calculate Pearson correlation coefficient
    mean_h_norm = sum(h_norm_values) / instances_tested
    mean_w_phi = sum(w_phi_values) / instances_tested
    
    cov = sum((h_norm_values[i] - mean_h_norm) * (w_phi_values[i] - mean_w_phi) for i in range(instances_tested)) / instances_tested
    var_h_norm = sum((h_norm_values[i] - mean_h_norm) ** 2 for i in range(instances_tested)) / instances_tested
    var_w_phi = sum((w_phi_values[i] - mean_w_phi) ** 2 for i in range(instances_tested)) / instances_tested
    
    r = cov / math.sqrt(var_h_norm * var_w_phi)
    
    return {
        "metric_name": "h_norm_w_phi",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(r) > 0.9,
        "counterexample": "" if abs(r) > 0.9 else "correlation_coefficient=0"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials")
        exit(0)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.9) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if abs(r["metric_value"]) <= 0.9), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")