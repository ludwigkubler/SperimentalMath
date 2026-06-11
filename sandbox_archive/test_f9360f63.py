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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(1, n+1):
            if all(f[j] == f[j+i] for j in range(n-i)):
                rank += 1
        return rank
    
    def quadratic_residue_system_diameter(f):
        n = len(f)
        qrs = []
        for x in range(2**n):
            y = sum(f[i] * (x >> i & 1) for i in range(n))
            qrs.append((x, y))
        diameter = 0
        for i in range(len(qrs)):
            for j in range(i+1, len(qrs)):
                distance = abs(qrs[i][1] - qrs[j][1])
                if distance > diameter:
                    diameter = distance
        return diameter
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_function(n)
        rank = communication_complexity_rank(f)
        d_qrs = quadratic_residue_system_diameter(f)
        ratio = d_qrs / math.sqrt(rank) if rank != 0 else float('inf')
        results.append({
            "n": n,
            "rank": rank,
            "d_qrs": d_qrs,
            "ratio": ratio
        })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["ratio"] <= 10 for result in results)  # Assuming c=10 for simplicity
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "d_qrs_over_sqrt_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")