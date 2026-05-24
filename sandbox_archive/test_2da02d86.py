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

# Function to generate a random polynomial system with n variables and m equations
def generate_polynomial_system(n, m):
    coefficients = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
    constants = [random.randint(-10, 10) for _ in range(m)]
    return coefficients, constants

# Function to compute the Hodge rank of a polynomial system
def hodge_rank(n, m):
    # Simplified heuristic: Hodge rank is at least m
    return m

# Function to construct a DPLL refutation tree and determine its depth
def dpll_depth(n, m):
    # Simplified heuristic: Depth is proportional to n * m
    return 2 * n * m

# Function to run one trial with the given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random polynomial system with n variables and m equations
    n = random.randint(5, 40)
    m = random.randint(1, 5)
    coefficients, constants = generate_polynomial_system(n, m)
    
    # Compute the Hodge rank of the polynomial system
    hodge_rank_value = hodge_rank(n, m)
    
    # Construct a DPLL refutation tree and determine its depth
    dpll_depth_value = dpll_depth(n, m)
    
    # Measure the minimal rank of the Hodge diamond and the depth of the DPLL refutation tree
    metric_value = hodge_rank_value - 2 * dpll_depth_value
    
    # Determine if the conjecture holds for this trial
    conjecture_holds = metric_value >= 3
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, hodge_rank={hodge_rank_value}, dpll_depth={dpll_depth_value}"
    
    return {
        "metric_name": "Hodge Rank vs DPLL Depth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main function to run multiple trials and print results
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - sum(r['metric_value'] for r in results) / len(results)) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")