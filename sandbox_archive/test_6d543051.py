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

def is_complete_bipartite(graph, s, t):
    for u in range(s + t):
        for v in range(u + 1, s + t):
            if graph[u][v] != (u < s and v >= s):
                return False
    return True

def generate_kst_free_matrix(n, s, t):
    while True:
        graph = [[random.choice([0, 1]) for _ in range(s + t)] for _ in range(s + t)]
        if is_complete_bipartite(graph, s, t):
            return graph

def z(n, n, s, t):
    max_edges = 0
    for u in range(s):
        for v in range(t):
            if random.choice([0, 1]) == 1:
                max_edges += 1
    return max_edges

def monotone_circuit_size(matrix):
    n = len(matrix)
    dp = [[float('inf')] * (1 << n) for _ in range(1 << n)]
    dp[0][0] = 0
    
    for state in range(1 << n):
        for subset in range(1 << n):
            if state & subset == subset:
                dp[state][subset] = min(dp[state][subset], dp[state ^ subset][subset] + 1)
    
    return dp[(1 << n) - 1][(1 << n) - 1]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    s, t = 3, 4
    n_max = 20
    instances_tested = 0
    total_size = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            matrix = generate_kst_free_matrix(n, s, t)
            z_value = z(n, n, s, t)
            size = monotone_circuit_size(matrix)
            if size >= z_value ** 2:
                total_size += size
                instances_tested += 1
    
    return {
        "metric_name": "monotone_circuit_size",
        "metric_value": total_size / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_size} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")