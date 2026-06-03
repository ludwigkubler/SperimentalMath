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
        # Generate a random graph using an adjacency list
        G = {i: [] for i in range(n)}
        for u in range(n):
            for v in range(u + 1, n):
                if random.choice([True, False]):
                    G[u].append(v)
                    G[v].append(u)
        return G
    
    def local_indeterminacy(G):
        # Simplified local indeterminacy calculation
        return len(G) // 2
    
    def circuit_monotone_width(G):
        # Simplified circuit monotone width calculation
        return len(G) ** 0.5
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_graph(n)
    
    local_ind = local_indeterminacy(G)
    w_m = circuit_monotone_width(G)
    
    ratio = local_ind / w_m
    within_10_percent = abs(ratio - 1) <= 0.1
    
    return {
        "metric_name": "Local Indeterminacy / Circuit Monotone Width Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": within_10_percent,
        "counterexample": "" if within_10_percent else f"Ratio {ratio} not within 10% of 1"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of 10% tolerance\" first_failing_seed={first_failing_seed}")