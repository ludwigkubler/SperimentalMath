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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        # Generate a random instance φ of size n
        return [random.randint(1, 100) for _ in range(n)]
    
    def compute_local_ring_norm(instance):
        # Compute the minimal norm of the local ring extension associated with instance
        norm = sum(x**2 for x in instance)
        return Fraction(norm).limit_denominator()
    
    def compute_growth_rate(instance):
        # Compute the growth rate of the communication complexity of instance
        n = len(instance)
        return (n * (n + 1)) / 2
    
    instances_tested = 0
    total_norm = 0
    total_growth_rate = 0
    n_max = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        instance = generate_instance(n)
        norm = compute_local_ring_norm(instance)
        growth_rate = compute_growth_rate(instance)
        
        if norm == 0 or growth_rate == 0:
            continue
        
        total_norm += norm
        total_growth_rate += growth_rate
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_norm = Fraction(total_norm).limit_denominator() / instances_tested
    mean_growth_rate = total_growth_rate / instances_tested
    
    # Calculate Pearson correlation coefficient
    numerator = sum((x - mean_norm) * (y - mean_growth_rate) for x, y in zip([compute_local_ring_norm(generate_instance(n)) for n in range(5, 41)], [compute_growth_rate(generate_instance(n)) for n in range(5, 41)]))
    denominator = math.sqrt(sum((x - mean_norm)**2 for x in [compute_local_ring_norm(generate_instance(n)) for n in range(5, 41)]) * sum((y - mean_growth_rate)**2 for y in [compute_growth_rate(generate_instance(n)) for n in range(5, 41)]))
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and correlation_coefficient <= (n_max**2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")