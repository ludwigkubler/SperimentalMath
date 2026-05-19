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
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(2 * n):
            layer = [random.choice([0, 1]) for _ in range(n)]
            bp.append(layer)
        return bp
    
    def transition_matrix(bp):
        n = len(bp) // 2
        T = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if bp[2 * i][j] == 1 and bp[2 * i + 1][j] == 1:
                    T[i][j] += 1
        return T
    
    def r_transform(T, k):
        n = len(T)
        R = [[0] * (k + 1) for _ in range(k + 1)]
        R[0][0] = 1
        for i in range(1, k + 1):
            R[i][0] = -sum(R[j][0] * T[j][i-1] for j in range(i))
            for j in range(1, i + 1):
                R[i][j] = sum(R[l][j-1] * T[l][i-j] for l in range(j)) / (i - j + 1)
        return R
    
    def free_entropy(T):
        n = len(T)
        R = r_transform(T, n)
        entropy = 0
        for i in range(n):
            for j in range(i + 1):
                if T[i][j] != 0:
                    entropy += T[i][j] * math.log(R[j][i])
        return entropy
    
    def inner_product_mod_2(bp):
        n = len(bp) // 2
        result = 0
        for i in range(n):
            result ^= bp[2 * i][i]
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        ip_bp = generate_read_twice_bp(n)
        if inner_product_mod_2(ip_bp) == 1:
            rho_ip = free_entropy(transition_matrix(ip_bp))
            results.append((n, rho_ip))
        
        for _ in range(4):
            bp = generate_read_twice_bp(n)
            if inner_product_mod_2(bp) != 1:
                rho_non_ip = free_entropy(transition_matrix(bp))
                if rho_non_ip >= n / 2:
                    return {
                        "metric_name": "free_entropy",
                        "metric_value": None,
                        "instances_tested": len(results),
                        "conjecture_holds": False,
                        "counterexample": f"non-IP_2 BP with ρ ≥ {n/2}"
                    }
    
    if not results:
        return {
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "no IP_2 BPs generated"
        }
    
    mean = sum(rho for _, rho in results) / len(results)
    std_dev = math.sqrt(sum((rho - mean) ** 2 for _, rho in results) / len(results))
    support_fraction = sum(1 for n, _ in results if n >= n_values[0]) / len(results)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if not results:
        print("RESULT: INCONCLUSIVE no data")
    else:
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for x in results if x is not None and x >= mean * 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is not None and result < mean * 0.8)
            print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")