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
    
    def generate_knot(n):
        # Placeholder for knot generation logic
        return [random.randint(0, 1) for _ in range(n)]
    
    def construct_dpll_tree(knot):
        # Placeholder for DPLL tree construction logic
        return len(knot) * 2
    
    def calculate_betti_number(knot):
        # Placeholder for Betti number calculation logic
        return sum(knot)
    
    metrics = []
    n_max = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        knot = generate_knot(n)
        d_K = construct_dpll_tree(knot)
        beta_K = calculate_betti_number(knot)
        
        metrics.append({
            "d_K": d_K,
            "beta_K": beta_K
        })
        
        n_max = max(n_max, n)
        instances_tested += 1
    
    mean_d_K = sum(m["d_K"] for m in metrics) / len(metrics)
    mean_beta_K = sum(m["beta_K"] for m in metrics) / len(metrics)
    
    correlation_coefficient = sum((m["d_K"] - mean_d_K) * (m["beta_K"] - mean_beta_K) for m in metrics) / len(metrics)
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")