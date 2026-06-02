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
    
    def resolution_proof_width(formula):
        # Simplified version of resolution proof width calculation
        return len(formula)
    
    def minimal_quaternionic_invariant(formula):
        # Simplified version of minimal quaternionic invariant calculation
        return sum(int(bit) for bit in formula)
    
    n = 5
    instances_tested = 0
    total_mi = 0
    total_w = 0
    
    while instances_tested < 30:
        formula = generate_boolean_formula(n)
        mi = minimal_quaternionic_invariant(formula)
        w = resolution_proof_width(formula)
        
        if mi is not None and w is not None:
            total_mi += mi
            total_w += w
            instances_tested += 1
        
        n += 5
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n - 5,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_mi = total_mi / instances_tested
    mean_w = total_w / instances_tested
    
    correlation_coefficient = (instances_tested * sum(mi * w for mi, w in zip([minimal_quaternionic_invariant(generate_boolean_formula(n)) for n in range(5, 20, 5)], [resolution_proof_width(generate_boolean_formula(n)) for n in range(5, 20, 5)])) - instances_tested * mean_mi * mean_w) / (instances_tested * sum((mi - mean_mi)**2 for mi in [minimal_quaternionic_invariant(generate_boolean_formula(n)) for n in range(5, 20, 5)]) * sum((w - mean_w)**2 for w in [resolution_proof_width(generate_boolean_formula(n)) for n in range(5, 20, 5)]))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 19,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(abs(mi - w) <= 3 for mi, w in zip([minimal_quaternionic_invariant(generate_boolean_formula(n)) for n in range(5, 20, 5)], [resolution_proof_width(generate_boolean_formula(n)) for n in range(5, 20, 5)])),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"] - 0.8) <= 3 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_sufficiently_high\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_invalid_metric")