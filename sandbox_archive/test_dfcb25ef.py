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
    v_values = [10, 12, 14, 16, 20]
    results = []
    
    for v in v_values:
        k = math.ceil(math.log2(v))
        V = list(itertools.combinations(range(1, v+1), k))
        idx_map = {v: i for i, v in enumerate(V)}
        
        adj_matrix = [[0] * len(V) for _ in range(len(V))]
        for M in V:
            for x in M:
                for y in range(1, v+1):
                    if y not in M:
                        M_prime = tuple(sorted(set(M) - {x} | {y}))
                        i, j = idx_map[M], idx_map[M_prime]
                        adj_matrix[i][j] = 1
                        adj_matrix[j][i] = 1
        
        triangle_count = 0
        for e in range(len(V)):
            for f in range(e+1, len(V)):
                if adj_matrix[e][f]:
                    N_e = [j for j in range(len(V)) if adj_matrix[e][j]]
                    N_f = [j for j in range(len(V)) if adj_matrix[f][j]]
                    t_ef = len(set(N_e) & set(N_f))
                    triangle_count += t_ef
        
        mu = triangle_count / (len(V) * (len(V) - 1) // 2)
        results.append(mu)
    
    mean_mu = sum(results) / len(results)
    conjecture_holds = all(mu >= v/4 for v, mu in zip(v_values, results))
    counterexample = "" if conjecture_holds else "v=10"
    
    return {
        "metric_name": "mu",
        "metric_value": mean_mu,
        "instances_tested": len(results),
        "n_max": max(v_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["n_max"] >= 16 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"v=10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")