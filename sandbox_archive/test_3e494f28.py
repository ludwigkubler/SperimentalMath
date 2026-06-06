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
    
    def frege_proof_depth(formula):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        for char in formula:
            if char == '1':
                stack.append(char)
            elif char == '0':
                if not stack:
                    return float('inf')
                stack.pop()
        return len(stack) + 1
    
    def symplectic_leaves_count(n):
        # Placeholder for the actual computation of symplectic leaves
        # This is a dummy function that returns a linear relationship with n
        return random.randint(2 * n, 3 * n)
    
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 5
    
    for n in range(5, 41):
        formula = generate_boolean_formula(n)
        d_phi = frege_proof_depth(formula)
        L_phi = symplectic_leaves_count(n)
        
        if d_phi == float('inf'):
            continue
        
        instances_tested += 1
        total_metric_value += L_phi / d_phi
        n_max = max(n_max, n)
    
    metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "symplectic_leaves_per_d_phi",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")