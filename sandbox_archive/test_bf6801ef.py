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
    n_values = [5, 10, 15, 20, 30, 40]
    gir_values = []
    
    for n in n_values:
        # Generate a random communication protocol φ with n bits
        phi = ''.join(random.choice('01') for _ in range(n))
        
        # Compute the metric embedding of the protocol using an established geometric invariant computation method
        # For simplicity, let's assume we have a function `compute_gir` that computes the geometric invariant rank
        gir = compute_gir(phi)
        
        gir_values.append(gir)
    
    if len(gir_values) < 30:
        return {
            "metric_name": "geometric_invariant_rank",
            "metric_value": float('inf'),
            "instances_tested": len(gir_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    # Analyze the correlation between gir(φ) and n to determine if |gir(φ)| is bounded by O(f(n))
    correlation_coefficient = compute_correlation(gir_values, n_values)
    
    return {
        "metric_name": "geometric_invariant_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(gir_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

def compute_gir(phi):
    # Placeholder function to compute the geometric invariant rank
    # In practice, this would involve complex computations based on the protocol φ
    return len(phi)  # Simplified example

def compute_correlation(gir_values, n_values):
    if len(gir_values) != len(n_values):
        raise ValueError("gir_values and n_values must have the same length")
    
    mean_gir = sum(gir_values) / len(gir_values)
    mean_n = sum(n_values) / len(n_values)
    
    numerator = sum((gir - mean_gir) * (n - mean_n) for gir, n in zip(gir_values, n_values))
    denominator = math.sqrt(sum((gir - mean_gir)**2 for gir in gir_values)) * math.sqrt(sum((n - mean_n)**2 for n in n_values))
    
    if denominator == 0:
        return float('nan')
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")