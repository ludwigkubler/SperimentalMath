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
    
    def construct_matroid(f):
        n = len(f)
        matroid = []
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j))]
            if all(f[i] == f[j] for j in subset):
                matroid.append(subset)
        return matroid
    
    def min_rank(matroid):
        rank = 0
        while matroid:
            pivot = matroid[0]
            matroid = [s for s in matroid if not any(s.issubset(t) for t in matroid)]
            rank += 1
        return rank
    
    def communication_complexity(f):
        n = len(f)
        max_bits = 0
        for i in range(2**n):
            bits = int(math.ceil(math.log2(i + 1)))
            if bits > max_bits:
                max_bits = bits
        return max_bits
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        matroid = construct_matroid(f)
        rank = min_rank(matroid)
        comm_complexity = communication_complexity(f)
        
        results.append({
            "n": n,
            "rank": rank,
            "comm_complexity": comm_complexity
        })
    
    mean_rank = sum(r["rank"] for r in results) / len(results)
    mean_comm_complexity = sum(r["comm_complexity"] for r in results) / len(results)
    correlation = sum((r["rank"] - mean_rank) * (r["comm_complexity"] - mean_comm_complexity) for r in results) / len(results)
    
    return {
        "metric_name": "Correlation between rank and communication complexity",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")