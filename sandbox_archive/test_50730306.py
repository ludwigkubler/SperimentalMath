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

def generate_planar_graph(n):
    if n <= 4:
        # Generate a small planar graph for n <= 4
        G = {i: [] for i in range(n)}
        if n == 3:
            G[0].append(1)
            G[1].append(0)
            G[1].append(2)
            G[2].append(1)
        elif n == 4:
            G[0].append(1)
            G[1].append(0)
            G[1].append(2)
            G[2].append(1)
            G[2].append(3)
            G[3].append(2)
    else:
        raise NotImplementedError("Mapping undefined for n > 4")
    return G

def min_geometric_entropy(G):
    # Placeholder function to compute minimal geometric entropy
    # This is a dummy implementation and should be replaced with actual computation
    return random.random()

def communication_complexity_rank(G):
    # Placeholder function to compute communication complexity rank
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    r_values = []
    
    for n in n_values:
        G = generate_planar_graph(n)
        h = min_geometric_entropy(G)
        r = communication_complexity_rank(G)
        
        h_values.append(h)
        r_values.append(r)
    
    if not h_values or not r_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_h = sum(h_values) / len(h_values)
    mean_r = sum(r_values) / len(r_values)
    
    covariance = sum((h - mean_h) * (r - mean_r) for h, r in zip(h_values, r_values)) / len(h_values)
    variance_h = sum((h - mean_h) ** 2 for h in h_values) / len(h_values)
    variance_r = sum((r - mean_r) ** 2 for r in r_values) / len(r_values)
    
    if variance_h == 0 or variance_r == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_h) * math.sqrt(variance_r))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")