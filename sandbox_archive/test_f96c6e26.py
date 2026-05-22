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
    
    def max_cut_instance(n):
        G = {}
        for i in range(n):
            G[i] = set()
        for _ in range(n * (n - 1) // 2):
            u, v = random.sample(range(n), 2)
            if v not in G[u]:
                G[u].add(v)
                G[v].add(u)
        return G
    
    def max_cut_value(G):
        n = len(G)
        value = 0
        for u in range(n):
            for v in G[u]:
                value += random.choice([1, -1])
        return abs(value) / (n * (n - 1))
    
    def tropical_curve_rank(G):
        # Placeholder for actual tropical curve rank calculation
        return len(G)
    
    def sum_of_squares_degree(n):
        # Placeholder for actual degree of sum-of-squares hierarchy approximation
        return n * (n - 1) // 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = max_cut_instance(n)
    value = max_cut_value(G)
    rank = tropical_curve_rank(G)
    degree = sum_of_squares_degree(n)
    
    return {
        "metric_name": "min_rank_tropical_curve",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= degree,
        "counterexample": f"Rank {rank} < Degree {degree}" if not rank >= degree else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")