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
    
    def generate_graph(n):
        edges = set()
        for _ in range(3 * n // 2):
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges
    
    def popcount(x):
        count = 0
        while x:
            count += x & 1
            x >>= 1
        return count
    
    def compute_cut_size_distribution(edges, n):
        a = [0] * (n + 1)
        for S in range(1 << n):
            mask = 0
            for i in range(n):
                if S & (1 << i):
                    mask ^= 1 << i
            count = popcount(mask)
            a[count] += 1
        return a
    
    def compute_LG(a, m):
        LG = [0] * (m + 1)
        for j in range(1, m):
            if a[j - 1] > 0 and a[j] > 0 and a[j + 1] > 0:
                LG[j] = math.log((a[j - 1] * a[j + 1]) / (a[j] ** 2))
        return max(LG)
    
    def compute_rho(n, lambda_max, MC):
        return n * lambda_max / (4 * MC) - 1
    
    n_values = [8, 10, 12, 14, 16, 18, 20]
    instances_tested = 0
    total_LD = 0.0
    total_rho = 0.0
    counterexample_found = False
    
    for n in n_values:
        for _ in range(30):
            edges = generate_graph(n)
            m = len(edges)
            a = compute_cut_size_distribution(edges, n)
            MC = max(a)
            lambda_max = max(math.eigvalsh(compute_LG(a, m)))[0]
            rho = compute_rho(n, lambda_max, MC)
            LD = compute_LG(a, m)
            
            instances_tested += 1
            total_LD += LD
            total_rho += rho
            
            if LD < 0.05 * rho:
                counterexample_found = True
                counterexample = f"n={n}, rho={rho:.4f}, LD={LD:.4f}"
    
    average_LD = total_LD / instances_tested
    average_rho = total_rho / instances_tested
    
    if counterexample_found:
        return {
            "metric_name": "Lorentzian Defect",
            "metric_value": average_LD,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "Lorentzian Defect",
            "metric_value": average_LD,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    total_LD = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    total_rho = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_LD:.4f} std=0.0000 support_fraction={support_fraction:.2f}")
    elif any(r["counterexample"] for r in results):
        counterexamples = [r["counterexample"] for r in results if r["counterexample"]]
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")