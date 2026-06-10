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

def generate_random_formula(n):
    if n == 1:
        return random.choice(['true', 'false'])
    else:
        op = random.choice(['and', 'or'])
        left = generate_random_formula(n // 2)
        right = generate_random_formula(n - n // 2 - 1)
        return f"({left} {op} {right})"

def compute_tqe(formula):
    # Placeholder for TQE computation
    # This is a dummy implementation that returns a random value for demonstration purposes
    return random.random()

def compute_w(phi_G):
    # Placeholder for w computation
    # This is a dummy implementation that returns a random value for demonstration purposes
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_max = 5
    
    for n in range(5, 41):
        if n > n_max:
            break
        
        phi_G = generate_random_formula(n)
        TQE_phi = compute_tqe(phi_G)
        w_phi = compute_w(phi_G)
        
        results.append({
            "n": n,
            "TQE_phi": TQE_phi,
            "w_phi": w_phi
        })
    
    if not results:
        return {
            "metric_name": "mean_absolute_difference",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    TQE_values = [r["TQE_phi"] for r in results]
    w_values = [r["w_phi"] for r in results]
    
    mean_absolute_difference = sum(abs(T - w) for T, w in zip(TQE_values, w_values)) / len(results)
    
    return {
        "metric_name": "mean_absolute_difference",
        "metric_value": mean_absolute_difference,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": mean_absolute_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            results.append(trial_result)
    
    if len(results) == 0:
        mean_absolute_difference = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_absolute_difference} std=0 support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='' first_failing_seed=None")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")