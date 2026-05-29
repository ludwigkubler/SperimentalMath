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
    def log2(x):
        return math.log2(x)

    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def choose(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))

    def powerset(s):
        result = []
        for r in range(len(s) + 1):
            for combo in itertools.combinations(s, r):
                result.append(frozenset(combo))
        return result

    def triangle_count(v, k, M1, M2):
        count = 0
        for i in range(v):
            if (i not in M1) and (i not in M2):
                M3 = M1.union({i})
                if len(M3.intersection(M2)) == k - 1:
                    count += 1
        return count

    def forman_ricci_proxy(v, k):
        V = list(powerset(range(v)))
        n = len(V)
        adj = [[] for _ in range(n)]
        for i in range(n):
            M = V[i]
            for x in M:
                for y in range(v):
                    if y not in M:
                        M_prime = M - {x} | {y}
                        j = V.index(M_prime)
                        adj[i].append(j)

        total_t_e_minus_k_minus_1 = 0
        for i in range(n):
            for j in adj[i]:
                t_e = triangle_count(v, k, V[i], V[j])
                total_t_e_minus_k_minus_1 += (t_e - (k - 1))

        return total_t_e_minus_k_minus_1 / len(adj)

    v_values = [10, 12, 14, 16, 20]
    results = []
    
    for v in v_values:
        k = math.ceil(log2(v))
        random.seed(seed)
        V = list(powerset(range(v)))
        n = len(V)
        adj = [[] for _ in range(n)]
        
        for i in range(n):
            M = V[i]
            for x in M:
                for y in range(v):
                    if y not in M:
                        M_prime = M - {x} | {y}
                        j = V.index(M_prime)
                        adj[i].append(j)

        total_t_e_minus_k_minus_1 = 0
        for i in range(n):
            for j in adj[i]:
                t_e = triangle_count(v, k, V[i], V[j])
                total_t_e_minus_k_minus_1 += (t_e - (k - 1))

        mu = total_t_e_minus_k_minus_1 / len(adj)
        results.append({
            "metric_name": "mu",
            "metric_value": mu,
            "instances_tested": n * len(adj),
            "n_max": v,
            "conjecture_holds": mu >= v / 4,
            "counterexample": "" if mu >= v / 4 else f"v={v}, mu={mu}"
        })

    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    mean_mu = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_mu = math.sqrt(sum((r["metric_value"] - mean_mu)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in all_results if r['conjecture_holds'] is False)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")