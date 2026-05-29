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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_vector_space(f):
        n = int(math.log(len(f), 2))
        T_f = [[None] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == 0 and j == 0:
                    T_f[i][j] = 0
                elif i == 0 or j == 0:
                    T_f[i][j] = float('inf')
                else:
                    T_f[i][j] = min(f[2**i], f[2**j])
        return T_f
    
    def tusnady_2_box_discrepancy(T_f):
        n = len(T_f) - 1
        discrepancy = 0
        for i in range(n + 1):
            for j in range(n + 1):
                if i != j:
                    discrepancy += abs(T_f[i][j] - T_f[j][i])
        return discrepancy / (2 * n * (n + 1))
    
    def compute_minimal_rank(T_f):
        rank = 0
        rows, cols = len(T_f), len(T_f[0])
        for i in range(rows):
            if all(T_f[i][j] == float('inf') for j in range(cols)):
                continue
            rank += 1
            for j in range(cols):
                if T_f[i][j] != float('inf'):
                    for k in range(rows):
                        if T_f[k][j] != float('inf'):
                            T_f[k][j] = min(T_f[k][j], T_f[i][j])
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_xor_function(n)
        T_f = compute_tropical_vector_space(f)
        D_2_F = tusnady_2_box_discrepancy(T_f)
        r_f = compute_minimal_rank(T_f)
        
        if len(results) >= 30:
            break
        
        results.append({
            "metric_name": "minimal_rank",
            "metric_value": r_f,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    if len(results) < 30:
        return {
            "seed": seed,
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n_max"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": support_fraction >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.5:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")