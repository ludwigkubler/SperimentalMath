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
    
    def generate_planar_graph(n):
        if n == 3:
            return [[1, 2], [2, 3], [3, 1]]
        elif n == 4:
            return [[1, 2], [2, 3], [3, 4], [4, 1], [1, 3]]
        else:
            raise NotImplementedError("Mapping undefined for n > 4")
    
    def geometric_entropy(G):
        # Placeholder function to compute geometric entropy
        return random.random()
    
    def communication_complexity_rank(G):
        # Placeholder function to compute communication complexity rank
        return len(G)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        G = generate_planar_graph(n)
        h_G = geometric_entropy(G)
        r_G = communication_complexity_rank(G)
        results.append((h_G, r_G))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    h_values = [h for h, _ in results]
    r_values = [r for _, r in results]
    
    mean_h = sum(h_values) / len(h_values)
    mean_r = sum(r_values) / len(r_values)
    covariance = sum((h - mean_h) * (r - mean_r) for h, r in results) / len(results)
    variance_h = sum((h - mean_h) ** 2 for h in h_values) / len(h_values)
    variance_r = sum((r - mean_r) ** 2 for r in r_values) / len(r_values)
    
    if variance_h == 0 or variance_r == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(G) for _, G in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_h) * math.sqrt(variance_r))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(len(G) for _, G in results),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")
    else:
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")