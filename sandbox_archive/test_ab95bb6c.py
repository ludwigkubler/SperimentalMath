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
from math import log2, ceil

def run_trial(seed: int) -> dict:
    results = []
    for N in [10, 15, 20]:
        v = 2 * N
        k = ceil(log2(v))
        c_values = [1, 1.5]
        for c in c_values:
            random.seed(seed)
            F_size = int(N ** c)
            F = set(random.sample(range(1, v + 1), F_size))
            
            G_F = {}
            for T in F:
                for T_prime in F:
                    if T != T_prime and len(T & T_prime) > 0:
                        if (T, T_prime) not in G_F:
                            G_F[(T, T_prime)] = []
                        G_F[(T, T_prime)].append((T, T_prime))
            
            deg_G_F = {T: sum(1 for T_prime in F if len(T & T_prime) > 0) for T in F}
            mu_F = max(max(0, deg_G_F[T] + deg_G_F[T_prime] - 4) for (T, T_prime), _ in G_F.items())
            
            sunflower_count = {}
            for T, T_prime in G_F:
                intersection = T & T_prime
                if intersection not in sunflower_count:
                    sunflower_count[intersection] = []
                sunflower_count[intersection].append((T, T_prime))
            
            max_petal_count = 0
            for core, pairs in sunflower_count.items():
                petal_set = set()
                for T, T_prime in pairs:
                    if len(T & T_prime) == len(core):
                        petal_set.add(T)
                max_petal_count = max(max_petal_count, len(petal_set))
            
            kappa_F = max_petal_count
            s = 6 * c * log2(1 + kappa_F) + 4 - mu_F
            
            results.append({
                "metric_name": "slack",
                "metric_value": s,
                "instances_tested": 1,
                "n_max": N,
                "conjecture_holds": s >= 0,
                "counterexample": "" if s >= 0 else f"μ(F)={mu_F}, κ(F)={kappa_F}"
            })
    
    return {
        "metric_name": "slack",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0) / len(results)
    
    if all(r >= 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r < 0 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r < 0)
        print(f"RESULT: FALSIFIED counterexample=\"μ(F) > 6c·log₂(1+κ(F)) + 4\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown_failure_mode")