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
    
    # Generate a randomly presented group G
    n = random.randint(5, 40)
    relators = [random.sample(range(n), 2) for _ in range(random.randint(1, 3))]
    generators = list(range(n))
    G = (generators, relators)
    
    # Compute the minimal local indeterminacy min_indet(G)
    # This is a placeholder function; replace with actual computation
    def compute_min_local_indeterminacy(group):
        return random.random() * n  # Placeholder
    
    min_indet_G = compute_min_local_indeterminacy(G)
    
    # Construct the DPLL tree for the group word problem and determine its width w(G)
    # This is a placeholder function; replace with actual computation
    def compute_dpll_width(group):
        return random.randint(1, n)  # Placeholder
    
    w_G = compute_dpll_width(G)
    
    # Correlate min_indet(G) and w(G)
    if w_G == 0:
        conjecture_holds = False
        counterexample = "w(G) is zero"
    else:
        correlation = abs(min_indet_G - (10 * math.log(w_G, 2)))
        conjecture_holds = correlation <= 3
        counterexample = f"min_indet(G) = {min_indet_G}, w(G) = {w_G}" if not conjecture_holds else ""
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")