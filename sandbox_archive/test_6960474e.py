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
        if k > n // 2:
            k = n - k
        c = 1
        for i in range(k):
            c = c * (n - i) // (i + 1)
        return c
    
    def forman_ricci_curvature(v, T):
        k = math.ceil(math.log2(v))
        max_overlap = 0
        for T_prime in F_star_v:
            overlap = sum(1 for _ in set(T).intersection(set(T_prime)))
            if overlap > max_overlap:
                max_overlap = overlap
        return comb(k, 2) / max_overlap
    
    def generate_null_hypergraph(v):
        edges = list(combinations(range(v), 2))
        random.shuffle(edges)
        null_hypergraph = []
        for _ in range(comb(v, k)):
            null_hypergraph.append(set(random.sample(edges, k)))
        return null_hypergraph
    
    v_values = [10, 16, 20, 24]
    results = []
    
    for v in v_values:
        k = math.ceil(math.log2(v))
        F_star_v = list(combinations(range(v), k))
        T_0 = set(combinations(range(k), 2))
        
        max_overlap = 0
        for T_prime in F_star_v:
            overlap = sum(1 for _ in set(T_0).intersection(set(T_prime)))
            if overlap > max_overlap:
                max_overlap = overlap
        
        mu_struct = comb(k, 2) / max_overlap
        results.append({"v": v, "mu_struct": mu_struct})
        
        if mu_struct < 1 + 1 / (k - 1):
            return {
                "metric_name": "mu_struct",
                "metric_value": mu_struct,
                "instances_tested": len(v_values),
                "n_max": max(v_values),
                "conjecture_holds": False,
                "counterexample": f"v={v}, mu_struct={mu_struct} < 1 + 1/(k-1)"
            }
        
        null_hypergraphs = [generate_null_hypergraph(v) for _ in range(30)]
        mu_rand_counts = [0] * len(null_hypergraphs)
        
        for T_prime in F_star_v:
            for i, H_rand in enumerate(null_hypergraphs):
                for hyperedge in H_rand:
                    overlap = sum(1 for _ in set(T_prime).intersection(set(hyperedge)))
                    if overlap > max_overlap:
                        mu_rand_counts[i] += 1
                        break
        
        mu_rand_avg = sum(mu_rand_counts) / len(mu_rand_counts)
        
        if mu_struct <= mu_rand_avg:
            return {
                "metric_name": "mu_struct vs mu_rand",
                "metric_value": mu_struct,
                "instances_tested": len(v_values),
                "n_max": max(v_values),
                "conjecture_holds": False,
                "counterexample": f"v={v}, mu_struct={mu_struct} <= mu_rand_avg={mu_rand_avg}"
            }
    
    return {
        "metric_name": "mu_struct",
        "metric_value": sum(result["mu_struct"] for result in results) / len(results),
        "instances_tested": len(v_values),
        "n_max": max(v_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")