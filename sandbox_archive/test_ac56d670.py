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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        for u in G:
            neighbors = [v for v in G if (u, v) in G or (v, u) in G]
            rank += len(neighbors)
        return rank // 2
    
    def minimal_rank(D):
        # Placeholder function; actual implementation depends on the specific design
        return len(D)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        D = G  # Placeholder; actual implementation depends on the specific design
        r_D = minimal_rank(D)
        kappa_G = communication_complexity_rank(G)
        
        if r_D < kappa_G + math.log2(n):
            counterexample = f"Graph with n={n} failed: r(D(G))={r_D}, κ(G)={kappa_G}, log(n)={math.log2(n)}"
            return {
                "metric_name": "minimal_rank",
                "metric_value": r_D,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append(r_D)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= kappa_G + math.log2(n)) / len(results)
    
    if all(r >= kappa_G + math.log2(n) for n, kappa_G, r in zip(n_values, [communication_complexity_rank(generate_random_graph(n)) for n in n_values], results)):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < kappa_G + math.log2(n) for n, kappa_G, r in zip(n_values, [communication_complexity_rank(generate_random_graph(n)) for n in n_values], results)):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='graph' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")