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
    v_values = [10, 16, 20, 24]
    results = []

    for v in v_values:
        k = math.ceil(math.log2(v))
        minterms = list(itertools.combinations(range(1, v + 1), k))
        n = len(minterms)
        
        if n < 30:
            return {
                "metric_name": "μ(F*_v)",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_minterms"
            }

        random.seed(seed + v)
        samples = [(random.choice(minterms), random.choice([x for x in minterms if len(set(x) - set(S)) == 1 and len(set(S) | {x[0]}) == k])) for _ in range(30)]
        
        min_mu_e = float('inf')
        counterexample = ""
        
        for S, T in samples:
            deg_S = k * (v - k)
            deg_T = k * (v - k)
            
            N_S = set()
            N_T = set()
            
            for S_prime in itertools.combinations(S, k-1):
                if len(set(S_prime) | {S[0]}) == k:
                    N_S.add(tuple(sorted(S_prime + (S[0],))))
            
            for T_prime in itertools.combinations(T, k-1):
                if len(set(T_prime) | {T[0]}) == k:
                    N_T.add(tuple(sorted(T_prime + (T[0],))))
            
            intersection_size = len(N_S & N_T)
            mu_e = -(4 - deg_S - deg_T + 3 * intersection_size)
            min_mu_e = min(min_mu_e, mu_e)
            
            if mu_e < v / 4 or mu_e > 2 * v * k:
                counterexample = f"(v={v}, S={S}, T={T}, μ_e={mu_e})"
        
        results.append({
            "metric_name": "μ(F*_v)",
            "metric_value": min_mu_e,
            "instances_tested": len(samples),
            "n_max": n,
            "conjecture_holds": v / 4 <= min_mu_e <= 2 * v * k,
            "counterexample": counterexample
        })
    
    return {
        "metric_name": "μ(F*_v)",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": sum(r["instances_tested"] for r in results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if r["counterexample"]), "")
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")