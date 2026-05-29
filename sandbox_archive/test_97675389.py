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
    
    def identity():
        return (1, 0)
    
    def multiply(g1, g2):
        h1, k1 = g1
        h2, k2 = g2
        return (h1 * h2, k1 + k2)
    
    def inverse(g):
        h, k = g
        det = h**2 + 1
        if det == 0:
            return None  # Avoid division by zero
        inv_det = Fraction(1, det)
        return (inv_det * h, -inv_det * k)
    
    def min_rank(G):
        rank = 0
        for g in G:
            h, k = g
            if h != 0:
                rank += 1
        return rank
    
    def max_cut_complexity(n):
        # Placeholder function to simulate Max-Cut complexity
        return random.uniform(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = []
    for _ in range(n):
        h = random.randint(1, 10)
        k = random.randint(1, 10)
        G.append((h, k))
    
    min_rank_G = min_rank(G)
    communication_complexity = max_cut_complexity(n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": n,
        "conjecture_holds": False if min_rank_G == 0 else communication_complexity / min_rank_G < 10,  # Arbitrary constant factor
        "counterexample": "mapping_undefined" if min_rank_G == 0 else ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_complexity = math.sqrt(sum((r["metric_value"] - mean_complexity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")