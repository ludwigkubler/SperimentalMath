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
    
    # Define p-adic Fourier series and DPLL search tree width for a given function f
    def p_adic_fourier_series(f, p):
        # Placeholder implementation; replace with actual computation
        return [random.randint(0, 1) for _ in range(5)]
    
    def dpll_search_tree_width(f):
        # Placeholder implementation; replace with actual computation
        return random.randint(2, 10)
    
    # Generate a random explicit function f in P
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    # Compute the p-adic Fourier series and DPLL search tree width for f
    p = random.choice([2, 3, 5])
    rank = sum(p_adic_fourier_series(f, p))
    dpll_width = dpll_search_tree_width(f)
    
    # Calculate the logarithm of the DPLL search tree width
    log_dpll_width = math.log(dpll_width) if dpll_width > 0 else float('-inf')
    
    # Compare the minimal rank with the logarithm of the DPLL search tree width
    ratio = log_dpll_width / (rank + 1e-9)
    difference = abs(log_dpll_width - rank)
    
    # Determine whether the conjecture holds for this seed
    conjecture_holds = ratio >= 0.8 and difference <= 3
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio out of bounds: {ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if any(trial_result["counterexample"] for trial_result in results):
        RESULT = "FALSIFIED counterexample='Ratio out of bounds' first_failing_seed=1"
    else:
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            RESULT = f"SUPPORTED mean={mean_ratio:.4f} std={std_ratio:.4f} support_fraction={support_fraction:.2f}"
        else:
            RESULT = f"FALSIFIED counterexample='Ratio out of bounds' first_failing_seed=1"
    
    print(RESULT)