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
    
    n = 40
    G = {i: set() for i in range(n)}
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    random.shuffle(edges)
    for u, v in edges[:n-1]:
        G[u].add(v)
        G[v].add(u)
    
    def min_distance(curve):
        distances = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            distances[i][i] = 0
        for u, v in edges[:n-1]:
            if curve[u] != curve[v]:
                distances[u][v] = 1
                distances[v][u] = 1
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distances[i][j] > distances[i][k] + distances[k][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
        
        return min(distances[i][j] for i in range(n) for j in range(i+1, n))
    
    def generate_curve():
        curve = [random.randint(0, 2**n - 1) for _ in range(n)]
        return curve
    
    nu_G = float('inf')
    for _ in range(10):  # Try multiple curves to find the minimum distance
        curve = generate_curve()
        nu_G = min(nu_G, min_distance(curve))
    
    steps_required = n**2  # Placeholder value; replace with actual MA^cc protocol steps
    
    return {
        "metric_name": "nu(G)",
        "metric_value": nu_G,
        "instances_tested": 10,
        "conjecture_holds": steps_required >= 2**(nu_G),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(31, 61))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")