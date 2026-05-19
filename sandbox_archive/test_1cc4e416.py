# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def compute_a_j(n, m):
        a = [0] * (m + 1)
        for subset in combinations(range(n), n // 2):
            subset_sum = sum(subset)
            if subset_sum < m:
                a[subset_sum] += 1
        return a
    
    def max_cut_size(a, m):
        return max(a[:m])
    
    def laplacian_eigenvalues(n, m):
        L = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            L[i][i - 1] = -1
            L[i][i] = 2
            L[i][i + 1] = -1
        eigenvalues = [0] * (n + 1)
        for i in range(n):
            eigenvalues[i] = math.eigenvalue(L, i)
        return max(eigenvalues[1:])
    
    def delorme_poljak_gap(n, m, lambda_max, mc):
        return n * lambda_max / (4 * mc) - 1
    
    def lorentzian_defect(a, m):
        ld = 0
        for j in range(1, m):
            if a[j - 1] > 0 and a[j] > 0 and a[j + 1] > 0:
                ld = max(ld, math.log((a[j - 1] * a[j + 1]) / (a[j] ** 2)))
        return ld
    
    n_values = [8, 10, 12, 14, 16, 18, 20]
    instances_tested = 0
    total_ld = 0.0
    total_rho = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = 3 * n // 2
        for _ in range(30):
            instances_tested += 1
            a_j_values = compute_a_j(n, m)
            mc = max_cut_size(a_j_values, m)
            lambda_max = laplacian_eigenvalues(n, m)
            rho = delorme_poljak_gap(n, m, lambda_max, mc)
            ld = lorentzian_defect(a_j_values, m)
            
            if rho >= 0.05 and ld < 0.05 * rho:
                conjecture_holds = False
                counterexample = f"(n={n}, rho={rho:.4f}, LD={ld:.4f})"
    
    mean_ld = total_ld / instances_tested if instances_tested > 0 else 0.0
    std_ld = math.sqrt(sum((ld - mean_ld) ** 2 for ld in a_j_values[:m]) / (instances_tested - 1)) if instances_tested > 1 else 0.0
    
    return {
        "metric_name": "Lorentzian Defect",
        "metric_value": mean_ld,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ld = sum(result["metric_value"] for result in results) / len(results)
    std_ld = math.sqrt(sum((result["metric_value"] - mean_ld) ** 2 for result in results) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ld:.4f} std={std_ld:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")