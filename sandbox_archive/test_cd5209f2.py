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

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate below
        factor = M[i][i]
        for k in range(n):
            if k != i:
                M[k][i] /= factor
        M[i][i] = Fraction(1)
        
        # Eliminate above
        for k in range(i-1, -1, -1):
            factor = M[k][i]
            for j in range(n):
                M[k][j] -= factor * M[i][j]
            M[k][i] = Fraction(0)
    return M

def coxeter_matrix_invariant(M):
    n = len(M)
    det = 1
    for i in range(n):
        det *= M[i][i]
    return abs(det)

def generate_read_twice_bp(size):
    # Simplified representation of a read-twice branching program
    bp = []
    for _ in range(size):
        bp.append(random.choice([0, 1]))
    return bp

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size = 2 ** n
        bp = generate_read_twice_bp(size)
        
        # Simulate the Coxeter group G associated with the BP (simplified)
        G = [[random.choice([1, -1]) for _ in range(n)] for _ in range(n)]
        
        # Compute the matrix invariant ρ(G)
        rho_G = coxeter_matrix_invariant(G)
        
        results.append({
            "n": n,
            "size": size,
            "rho_G": rho_G
        })
    
    if not results:
        return {
            "metric_name": "Coxeter Matrix Invariant vs BP_ReadTwice Circuit Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_sizes = [math.log(result["size"]) for result in results]
    rho_Gs = [result["rho_G"] for result in results]
    
    # Calculate Pearson correlation coefficient
    n = len(log_sizes)
    mean_log_size = sum(log_sizes) / n
    mean_rho_G = sum(rho_Gs) / n
    
    cov = sum((log_sizes[i] - mean_log_size) * (rho_Gs[i] - mean_rho_G) for i in range(n))
    var_log_size = sum((log_sizes[i] - mean_log_size) ** 2 for i in range(n))
    var_rho_G = sum((rho_Gs[i] - mean_rho_G) ** 2 for i in range(n))
    
    if var_log_size == 0 or var_rho_G == 0:
        return {
            "metric_name": "Coxeter Matrix Invariant vs BP_ReadTwice Circuit Size",
            "metric_value": None,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    corr_coeff = cov / (math.sqrt(var_log_size) * math.sqrt(var_rho_G))
    
    # Check if the trivial IP_2 function has an ρ(G) that is Ω(n)
    min_n = min(result["n"] for result in results)
    if any(rho_G < 0.5 * n for rho_G, n in zip(rho_Gs, log_sizes)):
        return {
            "metric_name": "Coxeter Matrix Invariant vs BP_ReadTwice Circuit Size",
            "metric_value": corr_coeff,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": f"Trivial IP_2 function has ρ(G) < 0.5 * n for some n"
        }
    
    return {
        "metric_name": "Coxeter Matrix Invariant vs BP_ReadTwice Circuit Size",
        "metric_value": corr_coeff,
        "instances_tested": n,
        "conjecture_holds": corr_coeff >= 0.7 and all(rho_G <= 10 * log_size for rho_G, log_size in zip(rho_Gs, log_sizes)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")