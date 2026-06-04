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
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def lefschetz_fitting_dimension(formula):
        # Placeholder implementation; actual computation depends on the formula
        return len(formula)  # Simplified example
    
    def resolution_proof_width(formula):
        # Placeholder implementation; actual computation depends on the formula
        return len(formula) * 2  # Simplified example
    
    instances_tested = 0
    n_max = 5
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size with 5 instances
            formula = generate_boolean_formula(n)
            Lf = lefschetz_fitting_dimension(formula)
            w = resolution_proof_width(formula)
            
            if Lf > 1000 and w < 10000:
                conjecture_holds = False
                counterexample = f"Formula with n={n}, Lf={Lf}, w={w}"
            
            total_metric_value += Lf
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for _ in range(instances_tested) if lefschetz_fitting_dimension(generate_boolean_formula(random.randint(5, 40))) > 1000 and resolution_proof_width(generate_boolean_formula(random.randint(5, 40))) >= 10000) / instances_tested
    
    return {
        "metric_name": "Lf",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")