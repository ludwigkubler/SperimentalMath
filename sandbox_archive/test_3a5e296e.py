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
    results = []
    for v in [10, 16, 20, 24]:
        k = math.ceil(math.log2(v))
        minterms = list(combinations(range(1, v + 1), k))
        n_minterms = len(minterms)
        
        if n_minterms == 0:
            return {
                "metric_name": "μ(F*_v)",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        def deg(S):
            return k * (v - k)
        
        def N(S):
            neighbors = []
            for S_prime in minterms:
                if len(set(S) & set(S_prime)) == k - 1:
                    neighbors.append(S_prime)
            return neighbors
        
        min_mu_e = float('inf')
        counterexample = ""
        
        random.seed(seed)
        for _ in range(30):
            S = random.choice(minterms)
            a = random.choice(list(S))
            b = random.choice([x for x in range(1, v + 1) if x != a and x not in S])
            T = tuple(sorted(set(S) - {a} | {b}))
            
            deg_S = deg(S)
            deg_T = deg(T)
            N_S = N(S)
            N_T = N(T)
            intersection_size = len(set(N_S) & set(N_T))
            
            mu_e = -(4 - deg_S - deg_T + 3 * intersection_size)
            if mu_e < min_mu_e:
                min_mu_e = mu_e
                counterexample = f"v={v}, S={S}, T={T}, μ_e={mu_e}"
        
        results.append({
            "v": v,
            "min_mu_e": min_mu_e
        })
    
    mean_mu = sum(result["min_mu_e"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["min_mu_e"] - mean_mu) ** 2 for result in results) / len(results))
    conjecture_holds = all(v / 4 <= result["min_mu_e"] <= 2 * v * k for result in results for v, k in [(10, 4), (16, 5), (20, 6), (24, 7)])
    
    return {
        "metric_name": "μ(F*_v)",
        "metric_value": mean_mu,
        "instances_tested": len(results),
        "n_max": max(v for v, k in [(10, 4), (16, 5), (20, 6), (24, 7)]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    mean_mu = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_mu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if v / 4 <= result["min_mu_e"] <= 2 * v * k for v, k in [(10, 4), (16, 5), (20, 6), (24, 7)]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_dev} support_fraction={support_fraction}")
    elif any(result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")