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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_monotone_width(f):
        n = int(math.log2(len(f)))
        max_width = 0
        for i in range(2**n):
            count = 0
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    count += 1
            max_width = max(max_width, count)
        return max_width
    
    def modular_symmetry_group(f):
        n = int(math.log2(len(f)))
        M = []
        for i in range(2**n):
            if all(f[i ^ (1 << j)] == f[i] for j in range(n)):
                M.append(i)
        return M
    
    def min_rank(M, f):
        n = int(math.log2(len(f)))
        rank = 0
        for g in M:
            count = sum(1 for j in range(n) if (g >> j) & 1)
            rank = max(rank, count)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        M = modular_symmetry_group(f)
        w_f = circuit_monotone_width(f)
        min_rank_M = min_rank(M, f)
        
        if abs(min_rank_M - w_f) > 10:
            return {
                "metric_name": "min_rank_M",
                "metric_value": min_rank_M,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, min_rank_M={min_rank_M}, w_f={w_f}"
            }
        
        results.append((min_rank_M, w_f))
    
    mean_min_rank_M = sum(x[0] for x in results) / len(results)
    std_min_rank_M = math.sqrt(sum((x[0] - mean_min_rank_M)**2 for x in results) / len(results))
    
    return {
        "metric_name": "min_rank_M",
        "metric_value": mean_min_rank_M,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": all(abs(x[0] - x[1]) <= 2 * x[1] for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_M not within a factor of 2 from w_f\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")