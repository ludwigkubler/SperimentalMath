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
    results = []
    for N in [10, 15, 20]:
        v = 2 * N
        k = math.ceil(math.log2(v))
        c_values = [1, 1.5]
        for c in c_values:
            random.seed(seed)
            F = set(random.sample(range(1, v + 1), int(N ** c)))
            G_F = {}
            for T in F:
                for T_prime in F:
                    if T != T_prime and len(T & T_prime) > 0:
                        if T not in G_F: G_F[T] = set()
                        if T_prime not in G_F: G_F[T_prime] = set()
                        G_F[T].add(T_prime)
                        G_F[T_prime].add(T)
            
            def degree(node):
                return len(G_F.get(node, set()))
            
            mu_F = max(max(0, degree(T) + degree(T_prime) - 4) for T in F for T_prime in F if T != T_prime and len(T & T_prime) > 0)
            
            sunflower_count = {}
            for T in F:
                core = frozenset(T)
                if core not in sunflower_count: sunflower_count[core] = []
                sunflower_count[core].append((T, degree(T)))
            
            def is_sunflower(core, terms):
                return all(len(term & core) == len(core) for term in terms)
            
            max_petal_count = 0
            for core, pairs in sunflower_count.items():
                terms = [pair[0] for pair in pairs]
                if is_sunflower(core, terms):
                    petal_count = len(terms)
                    if petal_count > max_petal_count:
                        max_petal_count = petal_count
            
            kappa_F = max_petal_count
            s = 6 * c * math.log2(1 + kappa_F) + 4 - mu_F
            results.append({"N": N, "c": c, "mu_F": mu_F, "kappa_F": kappa_F, "s": s})
    
    mean_s = sum(result["s"] for result in results) / len(results)
    std_s = math.sqrt(sum((result["s"] - mean_s) ** 2 for result in results) / len(results))
    conjecture_holds = all(result["s"] >= 0 for result in results)
    
    if conjecture_holds:
        return {
            "metric_name": "slack",
            "metric_value": mean_s,
            "instances_tested": len(results),
            "n_max": max(result["N"] for result in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["s"] < 0)
        return {
            "metric_name": "slack",
            "metric_value": mean_s,
            "instances_tested": len(results),
            "n_max": max(result["N"] for result in results),
            "conjecture_holds": False,
            "counterexample": f"seed={first_failing_seed}, N={results[first_failing_seed]['N']}, c={results[first_failing_seed]['c']}, mu_F={results[first_failing_seed]['mu_F']}, kappa_F={results[first_failing_seed]['kappa_F']}"
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_s = sum(result["metric_value"] for result in results) / len(results)
    std_s = math.sqrt(sum((result["metric_value"] - mean_s) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_s} std={std_s} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='seed={first_failing_seed}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")