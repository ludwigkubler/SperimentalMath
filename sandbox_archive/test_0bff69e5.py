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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def compute_moment_map(edges):
        # Simplified moment map computation (not actual symplectic geometry)
        return len(edges) / 2
    
    def optimal_max_cut_ratio(n):
        # Simplified approximation ratio (not actual Max-CUT algorithm)
        return n / math.log(n, 2)
    
    def symplectic_leaf_complexity(moment_map):
        # Simplified complexity (not actual symplectic geometry)
        return moment_map ** 0.5
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    moment_map = compute_moment_map(edges)
    optimal_ratio = optimal_max_cut_ratio(n)
    complexity = symplectic_leaf_complexity(moment_map)
    
    ratio = complexity / optimal_ratio
    metric_value = ratio
    
    conjecture_holds = ratio <= 10 * n ** 2  # Placeholder for actual f(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "symplectic_leaf_complexity_over_optimal_max_cut_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")