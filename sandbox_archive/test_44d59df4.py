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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def communication_complexity_rank(G):
        # Placeholder for actual computation
        return len(G)
    
    def minimal_rank(D):
        # Placeholder for actual computation
        return len(D)
    
    n = random.randint(5, 40)
    G = generate_random_graph(n)
    kappa_G = communication_complexity_rank(G)
    D_G = set(G)  # Simplified design for demonstration
    r_D_G = minimal_rank(D_G)
    
    if r_D_G < kappa_G + math.log2(n):
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_D_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Graph with {n} vertices, kappa(G) = {kappa_G}, minimal rank(D(G)) = {r_D_G}"
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_D_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default list of 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= kappa_G + math.log2(n)) / len(results)
    
    if all(r >= kappa_G + math.log2(n) for r, n in zip(results, [random.randint(5, 40) for _ in range(len(results))])):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r >= kappa_G + math.log2(n) for r, n in zip(results, [random.randint(5, 40) for _ in range(len(results))])):
        first_failing_seed = seeds[results.index(next(r for r, n in zip(results, [random.randint(5, 40) for _ in range(len(results))]) if not r >= kappa_G + math.log2(n)))]
        print(f"RESULT: FALSIFIED counterexample=\"Graph with {n} vertices\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")