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
    
    def comb(n, k):
        if k > n:
            return 0
        result = 1
        for i in range(k):
            result *= (n - i)
            result //= (i + 1)
        return result
    
    def forman_ricci_curvature(w_a, w_b, w_ab, w_f):
        if w_ab == 0:
            return float('inf')
        term1 = w_a + w_b
        term2 = sum(w_a / math.sqrt(w_ab * w_f) for f in range(1, w_ab))
        term3 = sum(w_b / math.sqrt(w_ab * w_f) for f in range(1, w_ab))
        return term1 - term2 - term3
    
    def orbit_count(v, k, j):
        return (1/2) * comb(v, k) * comb(k, j) * comb(v-k, k-j)
    
    def estimate_mu(v, k, num_samples=200):
        mu = 0
        for _ in range(num_samples):
            C_a = random.sample(range(v*(v-1)//2), k)
            C_b = random.sample(range(v*(v-1)//2), k)
            w_ab = sum(1 for a, b in zip(C_a, C_b) if (a, b) in edges or (b, a) in edges)
            F_j = forman_ricci_curvature(w_a, w_b, w_ab, 1)
            mu += orbit_count(v, k, j) * F_j
        return mu / sum(orbit_count(v, k, j) for j in range(k+1))
    
    v_values = [10, 16, 20, 24, 30, 40]
    results = []
    for v in v_values:
        k = math.ceil(math.log2(v))
        edges = set()
        for i in range(v):
            for j in range(i+1, v):
                if random.random() < 0.5:  # Generate a random graph
                    edges.add((i, j))
        
        mu = estimate_mu(v, k)
        if mu < v / 4:
            results.append({"seed": seed, "v": v, "mu": mu, "conjecture_holds": False, "counterexample": f"μ(F*_v)={mu} < v/4"})
            continue
        
        gap = mu - v / 4
        if not (0.05 * k <= gap <= 5 * k):
            results.append({"seed": seed, "v": v, "mu": mu, "conjecture_holds": False, "counterexample": f"gap={gap} not in [0.05k, 5k]"})
        else:
            results.append({"seed": seed, "v": v, "mu": mu, "conjecture_holds": True, "counterexample": ""})
    
    return {
        "metric_name": "Forman-Ricci Gap",
        "metric_value": sum(r["mu"] for r in results),
        "instances_tested": len(results),
        "n_max": max(v_values),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": "; ".join(r["counterexample"] for r in results if r["counterexample"])
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")