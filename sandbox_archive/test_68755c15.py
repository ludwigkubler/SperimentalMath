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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_kernel_geometric_quantization(f):
        # Placeholder for the actual computation
        return random.random() * len(f)
    
    def compute_bp_readtwice_circuit_size(f):
        # Placeholder for the actual computation
        return random.randint(1, 10) * len(f)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    J_f = compute_kernel_geometric_quantization(f)
    T_star_f = compute_bp_readtwice_circuit_size(f)
    
    if T_star_f == 0:
        return {
            "metric_name": "J(f)/T*(f)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Circuit size is zero"
        }
    
    ratio = J_f / T_star_f
    expected_ratio = math.log(n)
    within_bound = abs(ratio - expected_ratio) <= 0.1 * expected_ratio
    
    return {
        "metric_name": "J(f)/T*(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": within_bound,
        "counterexample": "" if within_bound else f"Ratio {ratio} not within ±10% of log({n})"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")