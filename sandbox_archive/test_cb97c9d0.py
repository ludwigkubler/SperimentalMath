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
        if k > n // 2:
            k = n - k
        res = 1
        for i in range(k):
            res *= (n - i)
            res //= (i + 1)
        return res
    
    def powerset(s):
        ps = []
        for r in range(len(s) + 1):
            for subset in itertools.combinations(s, r):
                ps.append(subset)
        return ps
    
    def overlap_neighbors(S, T, k):
        count = 0
        for U in G:
            if len(U & S) == k - 1 and len(U & T) == k - 1:
                count += 1
        return count
    
    v_values = [10, 16, 20, 24]
    results = []
    
    for v in v_values:
        k = math.ceil(math.log2(v))
        minterms = list(itertools.combinations(range(1, v + 1), k))
        G = {tuple(sorted(S)) for S in itertools.combinations(minterms, k - 1)}
        
        min_mu = float('inf')
        for _ in range(30):
            S = random.choice(minterms)
            T = None
            while True:
                a = random.choice(S)
                b = random.randint(1, v) if b not in S else random.choice([x for x in range(1, v + 1) if x != a and x not in S])
                T = tuple(sorted(set(S) - {a} | {b}))
                if T in G:
                    break
            
            deg_S = k * (v - k)
            deg_T = k * (v - k)
            N_S_intersect_N_T = overlap_neighbors(S, T, k)
            
            mu_e = -(4 - deg_S - deg_T + 3 * N_S_intersect_N_T)
            min_mu = min(min_mu, mu_e)
            
            if min_mu < v / 4 or min_mu > 2 * v * k:
                return {
                    "metric_name": "μ(F*_v)",
                    "metric_value": min_mu,
                    "instances_tested": 1,
                    "n_max": v,
                    "conjecture_holds": False,
                    "counterexample": f"(v={v}, S={S}, T={T}, μ_e={min_mu})"
                }
        
        results.append({
            "metric_name": "μ(F*_v)",
            "metric_value": min_mu,
            "instances_tested": 30,
            "n_max": v,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"mean_metric\": {result['mean_metric']:.6f}, \"std_metric\": {result['std_metric']:.6f}, \"support_fraction\": {result['support_fraction']:.2f}, \"conjecture_holds\": {result['support_fraction'] == 1.0}, \"counterexample\": \"{result.get('counterexample', '')}\"}}")
    
    if all(result["support_fraction"] == 1.0 for result in results):
        print(f"RESULT: SUPPORTED mean={result['mean_metric']:.6f} std={result['std_metric']:.6f} support_fraction=1.0")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_evidence")