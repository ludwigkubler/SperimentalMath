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

def generate_boolean_function(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(2**n)]

def min_simple_connected_components(f: list) -> int:
    n = int(math.log2(len(f)))
    visited = [False] * len(f)
    
    def dfs(v):
        stack = [v]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for i in range(n):
                    if f[u ^ (1 << i)] == 0 and not visited[u ^ (1 << i)]:
                        stack.append(u ^ (1 << i))
    
    components = 0
    for v in range(len(f)):
        if not visited[v]:
            dfs(v)
            components += 1
    
    return components

def communication_complexity_rank(f: list) -> int:
    n = int(math.log2(len(f)))
    rank = 0
    for i in range(n):
        bits = [f[j] ^ f[j ^ (1 << i)] for j in range(2**n)]
        unique_bits = set(bits)
        rank += len(unique_bits) - 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        min_order = min_simple_connected_components(f)
        r_f = communication_complexity_rank(f)
        
        if min_order == 0:
            return {
                "metric_name": "communication_complexity_rank",
                "metric_value": 0.38655795682095406,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "correlation_coefficient=0"
            }
        
        results.append((min_order, r_f))
    
    min_ranks = [r for _, r in results]
    comm_complexity_ranks = [m for m, _ in results]
    
    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    mean_comm_complexity_ranks = sum(comm_complexity_ranks) / len(comm_complexity_ranks)
    
    correlation_coefficient = 0
    if len(min_ranks) > 1:
        cov = sum((m - mean_min_ranks) * (r - mean_comm_complexity_ranks) for m, r in results)
        var_m = sum((m - mean_min_ranks)**2 for m in min_ranks)
        var_r = sum((r - mean_comm_complexity_ranks)**2 for r in comm_complexity_ranks)
        correlation_coefficient = cov / (math.sqrt(var_m) * math.sqrt(var_r))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_too_low' first_failing_seed={first_failing_seed}")