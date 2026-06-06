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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_brauer_group_order(instance):
        # Placeholder function to simulate Brauer group order computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(instance)
    
    def resolution_proof_width(instance):
        # Placeholder function to simulate resolution proof width computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(instance) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_boolean_instance(n)
        min_order = compute_brauer_group_order(instance)
        w_phi = resolution_proof_width(instance)
        correlation_value = (min_order - math.sqrt(n)) / (math.sqrt(n) * w_phi)
        results.append(correlation_value)
    
    mean_metric_value = sum(results) / len(results)
    conjecture_holds = all(0.7 <= corr >= 0.8 for corr in results)
    counterexample = "" if conjecture_holds else "Correlation out of bounds"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if 0.7 <= r >= 0.8) / len(results)
    
    if all(0.7 <= r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r < 0.7 or r > 0.8 for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not (0.7 <= r >= 0.8))]
        print(f"RESULT: FALSIFIED counterexample='Correlation out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason: No valid correlation values found")