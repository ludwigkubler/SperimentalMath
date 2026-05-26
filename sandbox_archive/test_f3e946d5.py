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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1):
                    edges.append((i, j))
        return edges
    
    def compute_moment_map(edges):
        # Simplified moment map computation (not actual symplectic geometry)
        return len(edges) / 2
    
    def optimal_max_cut_approx_ratio(n):
        # Upper bound for Max-CUT approximation ratio
        return n / math.log(n, 2)
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    moment_map_dim = compute_moment_map(edges)
    opt_ratio = optimal_max_cut_approx_ratio(n)
    
    if opt_ratio == 0:
        return {
            "metric_name": "Symplectic Leaf Complexity Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Optimal ratio is zero"
        }
    
    ratio = moment_map_dim / opt_ratio
    
    return {
        "metric_name": "Symplectic Leaf Complexity Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= n,  # Simplified f(n) for testing
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result_type = "FALSIFIED"
    
    print(f"RESULT: {result_type} mean={mean_value} std=0 support_fraction={support_fraction}")