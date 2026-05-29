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
    
    def comb(n, k):
        if k > n:
            return 0
        result = 1
        for i in range(k):
            result *= (n - i)
            result //= (i + 1)
        return result
    
    def max_overlap(T, F_v):
        max_overlap = 0
        for T_prime in F_v:
            if T != T_prime:
                overlap = sum(1 for _ in set(T) & set(T_prime))
                max_overlap = max(max_overlap, comb(overlap, 2))
        return max_overlap
    
    def forman_ricci_curvature(T, F_v):
        max_overlap_val = max_overlap(T, F_v)
        if max_overlap_val == 0:
            return float('inf')
        return comb(len(T), 2) / max_overlap_val
    
    def generate_null_hypergraph(v, k):
        edges = list(combinations(range(1, v+1), 2))
        null_edges = random.sample(edges, comb(v, 2) - comb(k, 2))
        return [frozenset(e) for e in null_edges]
    
    results = []
    for v in {10, 16, 20, 24}:
        k = math.ceil(math.log2(v))
        F_v = list(combinations(range(1, v+1), k))
        
        T_0 = frozenset(e for e in combinations(range(1, k+1), 2))
        max_overlap_val = max_overlap(T_0, F_v)
        mu_struct = comb(k, 2) / max_overlap_val
        results.append(mu_struct)
        
        if mu_struct < 1 + 1/(k-1):
            return {
                "metric_name": "mu_struct",
                "metric_value": mu_struct,
                "instances_tested": len(F_v),
                "n_max": k,
                "conjecture_holds": False,
                "counterexample": f"v={v}, k={k}"
            }
        
        null_hypergraphs = generate_null_hypergraph(v, k)
        mu_rand_count = 0
        for H_rand in null_hypergraphs:
            mu_rand_val = forman_ricci_curvature(H_rand[0], F_v)
            if mu_rand_val < mu_struct:
                mu_rand_count += 1
        
        if mu_rand_count > 5:
            return {
                "metric_name": "mu_struct",
                "metric_value": mu_struct,
                "instances_tested": len(F_v),
                "n_max": k,
                "conjecture_holds": False,
                "counterexample": f"v={v}, k={k}"
            }
    
    return {
        "metric_name": "mu_struct",
        "metric_value": sum(results) / len(results),
        "instances_tested": 4 * comb(v, 2) - comb(k, 2),
        "n_max": max([math.ceil(math.log2(v)) for v in {10, 16, 20, 24}]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 1 + 1/(math.ceil(math.log2(v)) - 1) for v in {10, 16, 20, 24}) / (len(results) * 4)
    
    if all(r >= 1 + 1/(math.ceil(math.log2(v)) - 1) for r in results for v in {10, 16, 20, 24}):
        print(f"RESULT: SUPPORTED mean={mean:.2f} std={std:.2f} support_fraction={support_fraction:.2f}")
    elif sum(r >= 1 + 1/(math.ceil(math.log2(v)) - 1) for r in results for v in {10, 16, 20, 24}) / (len(results) * 4) >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean:.2f} std={std:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not all(r >= 1 + 1/(math.ceil(math.log2(v)) - 1) for r in result for v in {10, 16, 20, 24}))
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")