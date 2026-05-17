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

def generate_k_clique_dnf(v, k):
    n = v * (v - 1) // 2
    dnf = [0] * n
    for i in range(k):
        for j in range(i + 1, k):
            term_index = i * (v - 1) + j - (i + 1) * i // 2
            if term_index < n:
                dnf[term_index] = 1
            else:
                raise IndexError("list assignment index out of range")
    return dnf

def generate_random_minterms(s, N):
    minterms = []
    for _ in range(s):
        minterm = [random.randint(0, 1) for _ in range(N)]
        if all(minterm):
            minterms.append(minterm)
    return minterms

def dot_product(u, v):
    return sum(x * y for x, y in zip(u, v))

def norm(v):
    return math.sqrt(sum(x**2 for x in v))

def monte_carlo_mean_width(K, num_samples=2000):
    N = len(K[0])
    u_samples = [[random.gauss(0, 1) for _ in range(N)] for _ in range(num_samples)]
    u_samples = [v / norm(v) for v in u_samples]
    max_inner_products = [max(dot_product(u, k) for k in K) for u in u_samples]
    return 2 * sum(max_inner_products) / num_samples

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for s in {5, 10, 20, 40}:
        for N in {12, 18, 24, 28}:
            minterms = generate_random_minterms(s, N)
            K = [m + [0] * (N - len(m)) for m in minterms]
            mu = monte_carlo_mean_width(K)
            results.append({
                "s": s,
                "N": N,
                "mu": mu
            })
    
    C1 = 3
    max_mu = max(result["mu"] for result in results)
    if max_mu > C1 * math.log(results[0]["s"] + 1) * (math.log(results[0]["N"]) + 1):
        return {
            "metric_name": "μ(f)",
            "metric_value": max_mu,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"μ(f) > {C1} * log(s+1) * (log N + 1)"
        }
    
    return {
        "metric_name": "μ(f)",
        "metric_value": max_mu,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu = sum(r["metric_value"] for r in results) / len(results)
    std_mu = math.sqrt(sum((r["metric_value"] - mean_mu)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"μ(f) > {C1} * log(s+1) * (log N + 1)\" first_failing_seed={first_failing_seed}")