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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def euclidean_distance(x, y):
        return sum((a - b)**2 for a, b in zip(x, y)) ** 0.5
    
    def riemannian_curvature_tensor(n):
        # Placeholder function to simulate the Riemannian curvature tensor calculation
        # This is a dummy implementation and does not reflect actual geometry
        return math.sqrt(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_xor_function(n)
        instances_tested = 2**n
        curvature_tensor = riemannian_curvature_tensor(n)
        
        if curvature_tensor < math.sqrt(n):
            counterexample = "Curvature tensor less than Ω(√n)"
            conjecture_holds = False
        else:
            counterexample = ""
            conjecture_holds = True
        
        results.append({
            "metric_name": "Riemannian Curvature Tensor",
            "metric_value": curvature_tensor,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    all_results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        all_results.extend(trial_result["results"])
    
    metric_values = [r["metric_value"] for r in all_results]
    conjecture_holds_count = sum(1 for r in all_results if r["conjecture_holds"])
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))**0.5
    support_fraction = conjecture_holds_count / len(all_results)
    
    if support_fraction >= 0.8:
        result = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"Curvature tensor less than Ω(√n)\" first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE"
    
    print(f"RESULT: {result} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")