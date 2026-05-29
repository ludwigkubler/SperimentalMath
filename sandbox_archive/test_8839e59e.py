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
    
    def generate_boolean_function(n):
        # Generate an arithmetic progression with n terms
        a = [random.randint(0, 1) for _ in range(n)]
        diff = set()
        for i in range(1, n):
            diff.add(a[i] - a[i-1])
        return a, len(diff)
    
    def tree_like_resolution_width(a):
        # Simplified version of the resolution width calculation
        max_width = 0
        current_width = 0
        for bit in a:
            if bit == 1:
                current_width += 1
                max_width = max(max_width, current_width)
            else:
                current_width = 0
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        a, S = generate_boolean_function(n)
        t_star = tree_like_resolution_width(a)
        upper_bound = math.log(S**2, 2)
        
        results.append({
            "metric_name": "t_star",
            "metric_value": t_star,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": t_star <= upper_bound,
            "counterexample": f"t_star={t_star}, upper_bound={upper_bound}" if not t_star <= upper_bound else ""
        })
    
    return {
        "metric_name": "t_star",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_t_star = sum(r["metric_value"] for r in results) / len(results)
    std_dev_t_star = math.sqrt(sum((r["metric_value"] - mean_t_star)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_t_star} std={std_dev_t_star} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])['counterexample']]}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")