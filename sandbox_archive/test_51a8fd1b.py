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
    
    def generate_knot(n):
        # Simple heuristic to generate a random knot with n crossings
        return [random.randint(0, n-1) for _ in range(n)]
    
    def dpll_search_tree(knot):
        # Simplified DPLL search tree construction (heuristic)
        if len(knot) == 1:
            return 1
        return 2 + max(dpll_search_tree(knot[:len(knot)//2]), dpll_search_tree(knot[len(knot)//2:]))
    
    def betti_number(knot):
        # Simplified Betti number calculation (heuristic)
        return len(set(knot)) - len(knot) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        knot = generate_knot(n)
        d_K = dpll_search_tree(knot)
        beta_K = betti_number(knot)
        metrics.append({"n": n, "d_K": d_K, "beta_K": beta_K})
        
        if len(metrics) >= 30:
            break
    
    correlation_coefficient = sum((m["d_K"] - mean_d_K) * (m["beta_K"] - mean_beta_K) for m in metrics) / len(metrics)
    mean_d_K = sum(m["d_K"] for m in metrics) / len(metrics)
    mean_beta_K = sum(m["beta_K"] for m in metrics) / len(metrics)
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(m["n"] for m in metrics),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")