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
    
    def generate_design(n, l, k, m):
        S = []
        while len(S) < m:
            block = set(random.sample(range(n), l))
            if all(len(block & s) <= k for s in S):
                S.append(block)
        return S
    
    def maj(z, S):
        count = 0
        for bit in z:
            if bit == 1:
                count += 1
            else:
                count -= 1
        return 1 if count >= 0 else 0
    
    def is_3ap(a, d, m):
        return (a + d) < m and (a + 2 * d) < m
    
    def estimate_rho3(D, n, l, k, m):
        samples = 1500
        rho3 = 0
        for _ in range(samples):
            z = [random.randint(0, 1) for _ in range(n)]
            counts = [maj(z, S) for S in D]
            for a in range(m):
                for d in range(1, m - a):
                    if is_3ap(a, d, m) and counts[a] == counts[a + d] == counts[a + 2 * d]:
                        rho3 += 1
        return rho3 / (samples * N3(m))
    
    def N3(m):
        return m * (m - 1) * (m - 2) // 6
    
    n_values = [20, 30, 40]
    l_values = [4, 6, 8]
    k_values = [1, 2, 3]
    m_values = [12, 20, 30]
    
    results = []
    for n in n_values:
        for l in l_values:
            for k in k_values:
                for m in m_values:
                    D = generate_design(n, l, k, m)
                    if len(D) != m:
                        continue
                    rho3 = estimate_rho3(D, n, l, k, m)
                    results.append({
                        "n": n,
                        "l": l,
                        "k": k,
                        "m": m,
                        "rho3": rho3
                    })
    
    if not results:
        return {
            "metric_name": "rho3",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_designs"
        }
    
    k_over_l_sqrt = [(k / l) ** 0.5 for n, l, k, m, rho3 in results]
    rho3_minus_half = [rho3 - 0.25 for n, l, k, m, rho3 in results]
    
    if len(k_over_l_sqrt) < 10:
        return {
            "metric_name": "rho3",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    r = pearson_correlation(k_over_l_sqrt, rho3_minus_half)
    R = [rho3_val / k_over_l_sqrt_val for k_over_l_sqrt_val, rho3_val in zip(k_over_l_sqrt, rho3_minus_half)]
    max_R = max(R)
    min_R = min(R)
    
    return {
        "metric_name": "rho3",
        "metric_value": r,
        "instances_tested": len(results),
        "conjecture_holds": r >= 0.7 and max_R / min_R <= 8,
        "counterexample": "" if r >= 0.7 and max_R / min_R <= 8 else f"max(R)/min(R) = {max_R}/{min_R}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = [run_trial(seed) for seed in seeds if "conjecture_holds" in trial and trial["conjecture_holds"]]
    if not results:
        print("RESULT: INCONCLUSIVE no_valid_results")
    else:
        r_values = [trial["metric_value"] for trial in results]
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={sum(r_values)/len(r_values)} std={math.sqrt(sum((r - sum(r_values)/len(r_values))**2 for r in r_values)/len(r_values))} support_fraction={support_fraction}")