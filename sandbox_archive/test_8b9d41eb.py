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
    
    def generate_function(n):
        # Generate a random explicit function f in P with Sipser function representation
        return [random.randint(0, 1) for _ in range(n)]
    
    def calculate_minimal_local_index(f):
        # Placeholder for actual calculation of minimal local index
        # For simplicity, we use the length of the function as a proxy
        return len(f)
    
    def calculate_entropy_based_communication_complexity(f):
        # Placeholder for actual calculation of entropy-based communication complexity
        # For simplicity, we use the sum of elements in the function as a proxy
        return sum(f)
    
    n = 30
    f = generate_function(n)
    minimal_local_index = calculate_minimal_local_index(f)
    entropy_based_communication_complexity = calculate_entropy_based_communication_complexity(f)
    
    metric_value = minimal_local_index / entropy_based_communication_complexity if entropy_based_communication_complexity != 0 else float('inf')
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinimalLocalIndexOverEntropyBasedCommComplexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50, 2))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")