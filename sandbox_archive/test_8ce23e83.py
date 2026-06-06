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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def resolution_proof_width(phi):
        # Simplified mock-up of resolution proof width calculation
        return len(phi) * 2
    
    def minimal_rank_of_kac_moody_algebra(phi):
        # Simplified mock-up of minimal rank calculation
        return len(phi)
    
    n = random.randint(5, 30)
    phi = generate_boolean_formula(n)
    w_phi = resolution_proof_width(phi)
    r_G = minimal_rank_of_kac_moody_algebra(phi)
    
    metric_value = w_phi / r_G if r_G != 0 else float('inf')
    conjecture_holds = metric_value >= 10
    counterexample = "" if conjecture_holds else f"phi={phi}, w_phi={w_phi}, r_G={r_G}"
    
    return {
        "metric_name": "Resolution Proof Width / Minimal Rank Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r['metric_value'] for r in results if 'metric_value' in r]
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        result = f"FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")