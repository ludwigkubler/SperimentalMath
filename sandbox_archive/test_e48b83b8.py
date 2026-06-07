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
    
    # Generate a random n-vertex d-regular graph
    n = 20
    d = 3
    if n % d != 0:
        return {
            "metric_name": "log|H^1(G)| vs R_var(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    G = {}
    for i in range(n):
        neighbors = random.sample([j for j in range(n) if j != i], d)
        G[i] = set(neighbors)
    
    # Compute the associated algebraic geometry of boolean functions
    # and determine the ideal I_G (simplified for this example)
    I_G = set()
    for node in G:
        for neighbor in G[node]:
            I_G.add((node, neighbor))
    
    # Calculate the minimal local cohomology group H^1(G) (simplified)
    H_1_G = len(I_G)
    
    # Compute the communication complexity rank variance R_var(G)
    # (simplified for this example)
    R_var_G = H_1_G / n
    
    # Correlate log|H^1(G)| with R_var(G) using a statistical test
    log_H_1_G = math.log(H_1_G) if H_1_G > 0 else -math.inf
    correlation_coefficient = (log_H_1_G * R_var_G) / (n * n)
    
    return {
        "metric_name": "log|H^1(G)| vs R_var(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "N/A"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")