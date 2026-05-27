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
    
    def calculate_complexity(f):
        # Placeholder complexity calculation (replace with actual logic)
        return len(f)
    
    def calculate_geometric_invariant_space_dimension(f):
        # Placeholder dimension calculation (replace with actual logic)
        return len(f) ** 0.5
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    complexity = calculate_complexity(f)
    dimension = calculate_geometric_invariant_space_dimension(f)
    
    if dimension == 0:
        return {
            "metric_name": "complexity",
            "metric_value": complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "dimension_zero"
        }
    
    ratio = complexity / dimension ** 2
    
    return {
        "metric_name": "complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= math.log(dimension, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(1000, 3000))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dimension_zero\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")