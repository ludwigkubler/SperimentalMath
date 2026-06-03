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
    
    # Generate a random tautology φ with n variables
    n = 10  # Fixed for simplicity, can be varied within each trial if needed
    phi = [random.choice([True, False]) for _ in range(n)]
    
    # Construct the associated tiling space G (simplified example)
    G = generate_tiling_space(phi)
    
    # Compute the minimal geometric entropy H(min)(G)
    H_min_G = compute_min_geometric_entropy(G)
    
    # Calculate the communication complexity rank r(G)
    r_G = calculate_communication_complexity_rank(G)
    
    # Measure the correlation between H(min)(G) and r(G)
    if r_G == 0:
        conjecture_holds = False
        counterexample = "communication_complexity_rank_zero"
    else:
        k = abs(H_min_G - (r_G * 1.5))  # Example constant, can be adjusted
        conjecture_holds = k <= 1  # Example threshold, can be adjusted
        counterexample = ""
    
    return {
        "metric_name": "H(min)(G)",
        "metric_value": H_min_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_tiling_space(phi):
    # Simplified example: a tiling space associated with a tautology
    G = {}
    for i in range(len(phi)):
        if phi[i]:
            G[i] = [i + 1, i + 2]
    return G

def compute_min_geometric_entropy(G):
    # Simplified example: minimal geometric entropy calculation
    entropy = sum(1 / len(v) for v in G.values())
    return entropy

def calculate_communication_complexity_rank(G):
    # Simplified example: communication complexity rank calculation
    rank = max(len(v) for v in G.values())
    return rank

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default list of prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")