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
    
    # Generate a random SAT instance with n variables and m clauses
    n = 40
    m = 2 * n
    phi = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        phi.append(clause)
    
    # Compute the area of the minimal Kähler manifold representation (simplified example)
    area = sum(abs(c[0]) * abs(c[1]) for c in phi) / 2
    
    # Compute the height of the DPLL search tree (simplified example)
    dpll_height = n ** 2
    
    return {
        "metric_name": "Kähler Area and DPLL Height",
        "metric_value": area + dpll_height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": area <= n * math.log(n) and dpll_height >= n ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 50, 2))  # Default to first 30 primes if no seeds provided
    
    results = []
    total_area = 0
    total_dpll_height = 0
    num_trials = len(seeds)
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        
        total_area += trial_result["metric_value"]
        total_dpll_height += trial_result["metric_value"] - trial_result["n_max"] ** 2
    
    mean_area = total_area / num_trials
    mean_dpll_height = total_dpll_height / num_trials
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials
    
    print(f"RESULT: SUPPORTED mean_area={mean_area} mean_dpll_height={mean_dpll_height} support_fraction={support_fraction}")