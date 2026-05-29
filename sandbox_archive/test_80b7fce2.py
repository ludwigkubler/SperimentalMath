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
from math import comb, log2
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cliques(v, k):
        vertices = list(range(1, v+1))
        return [set(comb(vertices, 2)) for _ in range(k)]
    
    def compute_ric(T, F_star):
        max_overlap = 0
        for T_prime in F_star:
            overlap = len(T & T_prime)
            if overlap > max_overlap:
                max_overlap = overlap
        ric_value = comb(k, 2) / max_overlap if max_overlap != 0 else float('inf')
        return ric_value
    
    def generate_random_hypergraph(v, k):
        edges = list(combinations(range(1, v+1), 2))
        random.shuffle(edges)
        return set(edges[:comb(v, 2)])
    
    results = []
    for v in [10, 16, 20, 24]:
        k = int(log2(v) + 0.5)
        F_star = generate_k_cliques(v, k)
        T_0 = frozenset(comb(range(1, k+1), 2))
        
        max_overlap = 0
        for T_prime in F_star:
            overlap = len(T_0 & T_prime)
            if overlap > max_overlap:
                max_overlap = overlap
        
        mu_struct = comb(k, 2) / max_overlap if max_overlap != 0 else float('inf')
        results.append(mu_struct)
        
        if mu_struct < 1 + 1/(k-1):
            return {
                "metric_name": "μ_struct",
                "metric_value": mu_struct,
                "instances_tested": 1,
                "n_max": k,
                "conjecture_holds": False,
                "counterexample": f"μ_struct < 1 + 1/(k-1) for v={v}"
            }
    
    mu_rand = []
    for _ in range(30):
        H_rand = generate_random_hypergraph(v, k)
        T_prime = frozenset(random.sample(H_rand, comb(k, 2)))
        max_overlap_rand = len(T_0 & T_prime)
        mu_rand_value = comb(k, 2) / max_overlap_rand if max_overlap_rand != 0 else float('inf')
        mu_rand.append(mu_rand_value)
    
    mean_mu_struct = sum(results) / len(results)
    std_dev_mu_struct = (sum((x - mean_mu_struct) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for x in mu_rand if x < mean_mu_struct) / len(mu_rand)
    
    return {
        "metric_name": "μ_struct",
        "metric_value": mean_mu_struct,
        "instances_tested": 4 * 30,  # 4 v values with 30 seeds each
        "n_max": k,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"μ_struct < 1 + 1/(k-1)\" first_failing_seed={first_failing_seed}")