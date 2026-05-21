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
    
    def log2(x):
        return math.log2(x) if x > 0 else float('inf')
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def sigma_max(A):
        U, _, Vt = gaussian_elimination([[A[i][j] ** 2 for j in range(len(A[0]))] for i in range(len(A))])
        return math.sqrt(sum(U[i][i] for i in range(min(len(U), len(Vt)))))
    
    def generate_design(n):
        l = math.ceil(log2(n))
        k = math.ceil(log2(log2(n)))
        m = n // (2 * k + 1)
        design = []
        while len(design) < m:
            S = set(random.sample(range(1, n+1), l))
            if all(len(S & T) <= k for T in design):
                design.append(S)
        return design
    
    def build_sigma_n(f, D):
        m = len(D)
        Sigma = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i+1, m):
                S_i, S_j = D[i], D[j]
                if f(S_i, S_j) == 1:
                    Sigma[i][j] = -1
                else:
                    Sigma[i][j] = 1
        return Sigma
    
    def DISJ(S1, S2):
        return len(S1 & S2) == 0
    
    def EQ(S1, S2):
        return S1 == S2
    
    def INNER_PRODUCT(S1, S2):
        return sum(1 for x in range(1, max(max(S1), max(S2)) + 1) if x in S1 and x in S2)
    
    def GREATER_THAN(S1, S2):
        return len(S1 - S2) > len(S2 - S1)
    
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    results = []
    
    for n in n_values:
        design = generate_design(n)
        sigma_disj = build_sigma_n(DISJ, design)
        sigma_eq = build_sigma_n(EQ, design)
        sigma_ip = build_sigma_n(INNER_PRODUCT, design)
        sigma_gt = build_sigma_n(GREATER_THAN, design)
        
        rho_disj = sigma_max(sigma_disj) / len(design)
        rho_eq = sigma_max(sigma_eq) / len(design)
        rho_ip = sigma_max(sigma_ip) / len(design)
        rho_gt = sigma_max(sigma_gt) / len(design)
        
        results.append({
            "n": n,
            "rho_DISJ": rho_disj,
            "rho_EQ": rho_eq,
            "rho_IP": rho_ip,
            "rho_GT": rho_gt
        })
    
    all_rho_disj_valid = all(rho["rho_DISJ"] * math.sqrt(len(design)) <= 4 for rho in results)
    all_rho_eq_valid = all(rho["rho_EQ"] >= 1 - 6 / len(design) for rho in results)
    
    conjecture_holds = all_rho_disj_valid and all_rho_eq_valid
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "normalized spectral discrepancy",
        "metric_value": sum(rho["rho_DISJ"] * math.sqrt(len(design)) for rho in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")