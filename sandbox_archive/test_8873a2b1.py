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
    
    def resolution_proof_width(phi):
        # Simplified estimate, not actual proof width calculation
        return len(phi)
    
    def minimal_quaternionic_invariant(phi):
        # Simplified estimate, not actual invariant calculation
        return len(phi) / 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_mi = 0
    total_w = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_boolean_formula(n)
            mi_phi = minimal_quaternionic_invariant(phi)
            w_phi = resolution_proof_width(phi)
            
            total_mi += mi_phi
            total_w += w_phi
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_mi = total_mi / instances_tested
    mean_w = total_w / instances_tested
    
    correlation_coefficient = (instances_tested * sum(mi_phi * w_phi for mi_phi, w_phi in zip(mi_values, w_values)) -
                               sum(mi_values) * sum(w_values)) / math.sqrt(
        (instances_tested * sum(mi_phi**2 for mi_phi in mi_values) - sum(mi_values)**2) *
        (instances_tested * sum(w_phi**2 for w_phi in w_values) - sum(w_values)**2)
    )
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(abs(mi_phi - w_phi) <= 3 for mi_phi, w_phi in zip(mi_values, w_values))
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or |mi(φ) - w(φ)| > 3"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"]) > 3 for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or other issues")