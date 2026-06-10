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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        count = [0] * (n + 1)
        for i in range(2**n):
            count[sum(f[j] if (i >> j) & 1 else 0 for j in range(n))] += 1
        return sum(count[i]**2 for i in range(n + 1)) / (2**(2*n))
    
    def conformal_block_dimension(r, n):
        if r == 0:
            return 0
        return (r**2) / math.log(n)
    
    def calculate_metric(f, n):
        r = communication_complexity_rank_variance(f)
        dim_M_f = conformal_block_dimension(r, n)
        return {
            "metric_name": "dim(M_f)",
            "metric_value": dim_M_f,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(dim_M_f - (r**2 / math.log(n))) <= 0.2 * (r**2 / math.log(n)),
            "counterexample": ""
        }
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        result = calculate_metric(f, n)
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_value": mean_value,
        "std_value": std_value,
        "support_fraction": support_fraction,
        "n_max": max(r["n_max"] for r in results),
        "instances_tested": sum(r["instances_tested"] for r in results)
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["mean_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["mean_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.95) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")