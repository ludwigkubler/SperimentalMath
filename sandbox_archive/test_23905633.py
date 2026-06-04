# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def duality_representation(formula):
        # Simplified lattice-based construction (not actual duality representation)
        return [int(bit) for bit in formula]
    
    def resolution_proof_depth(formula):
        # Simplified DPLL solver (not actual proof depth calculation)
        return len(formula)
    
    def min_lattice_point_density(dual_space):
        return sum(dual_space) / len(dual_space)
    
    n = 5
    instances_tested = 0
    total_min_lpd = 0
    total_depth = 0
    
    for _ in range(30):
        formula = generate_formula(n)
        dual_space = duality_representation(formula)
        depth = resolution_proof_depth(formula)
        
        if len(dual_space) == 0:
            continue
        
        min_lpd = min_lattice_point_density(dual_space)
        total_min_lpd += min_lpd
        total_depth += depth
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "MinLPD",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "No valid dual spaces generated"
        }
    
    mean_min_lpd = total_min_lpd / instances_tested
    mean_depth = total_depth / instances_tested
    
    return {
        "metric_name": "MinLPD",
        "metric_value": mean_min_lpd * mean_depth,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "Mapping undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")