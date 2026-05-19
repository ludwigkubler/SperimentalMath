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
    
    def compute_LG(a, m):
        n = len(a)
        LG = [[0] * (n + 1) for _ in range(n + 1)]
        LG[0][0] = 1
        for j in range(1, n + 1):
            LG[j][0] = a[j - 1]
            for k in range(1, j + 1):
                LG[j][k] = (LG[j - 1][k - 1] + LG[j - 1][k]) * m
        return LG
    
    def compute_a_j(n, m):
        a = [0] * (n + 1)
        for S in range(1 << n):
            subset_sum = sum(a[i] for i in range(n) if S & (1 << i))
            a[subset_sum] += 1
        return a
    
    def compute_MC(G):
        return max(abs(delta_G(S, G)) for S in range(1 << len(G)))
    
    def delta_G(S, G):
        return sum(a_j(G, S, j) for j in range(len(G) + 1))
    
    def a_j(G, S, j):
        count = 0
        for subset in range(1 << len(G)):
            if (subset & S == S) and (len(subset ^ S) == j):
                count += 1
        return count
    
    def compute_lambda_max(LG):
        n = len(LG)
        A = [[LG[i][j] - LG[i + 1][j] for j in range(n)] for i in range(n - 1)]
        eigenvalues = [0] * (n - 1)
        for k in range(n - 1):
            max_val = float('-inf')
            for i in range(k, n - 1):
                if A[i][k] > max_val:
                    max_val = A[i][k]
                    idx = i
            eigenvalues[k], A[idx][k] = A[idx][k], eigenvalues[k]
            for j in range(k + 1, n - 1):
                A[j][k] /= eigenvalues[k]
            for i in range(k + 1, n - 1):
                for j in range(k + 1, n - 1):
                    A[i][j] -= A[i][k] * A[k][j]
        return max(eigenvalues)
    
    def compute_rho(G, lambda_max, MC):
        return len(G) * lambda_max / (4 * MC) - 1
    
    def compute_LD(G, a_j_values):
        m = len(a_j_values) - 1
        LD = float('-inf')
        for j in range(1, m):
            if a_j_values[j - 1] > 0 and a_j_values[j] > 0 and a_j_values[j + 1] > 0:
                ratio = (a_j_values[j - 1] * a_j_values[j + 1]) / (a_j_values[j] ** 2)
                if ratio > LD:
                    LD = math.log(ratio)
        return max(0, LD)
    
    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        m = 3 * n // 2
        C_m_j = math.comb(m, (m + n) // 2)
        
        for _ in range(30):
            a_j_values = compute_a_j(n, m)
            MC = compute_MC(a_j_values)
            lambda_max = compute_lambda_max(compute_LG(a_j_values, m))
            rho_G = compute_rho(a_j_values, lambda_max, MC)
            LD_G = compute_LD(a_j_values, a_j_values)
            
            results.append({
                "n": n,
                "rho_G": rho_G,
                "LD_G": LD_G
            })
    
    all_supported = True
    for result in results:
        if result["LD_G"] < 0.05 * result["rho_G"]:
            all_supported = False
            break
    
    return {
        "metric_name": "Lorentzian Defect of Cut Polynomial Lower-Bounds Max-CUT SoS-2 Gap",
        "metric_value": sum(result["LD_G"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all_supported,
        "counterexample": "" if all_supported else f"n={result['n']}, rho(G)={result['rho_G']:.4f}, LD(G)={result['LD_G']:.4f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['n']}, rho(G)={result['rho_G']:.4f}, LD(G)={result['LD_G']:.4f}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")