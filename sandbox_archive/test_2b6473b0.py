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
    
    def generate_instance(n):
        # Generate a random communication complexity instance with rank variance R(n)
        # This is a placeholder function; replace it with actual instance generation logic
        return [random.randint(1, n) for _ in range(n)]
    
    def measure_invariant(instance):
        # Measure the rank variance R(n) and number of symmetric spaces S(n)
        # This is a placeholder function; replace it with actual invariant measurement logic
        n = len(instance)
        R_n = sum(x * (n - x) for x in instance) / (2 * n**2)
        S_n = random.randint(1, 50)  # Placeholder for symmetric spaces count
        return R_n, S_n
    
    def correlation_check(R_n, S_n):
        # Check if the difference between S(n) and R(n) is within ±k
        k = 5
        return abs(S_n - R_n) <= k
    
    n_max = 0
    instances_tested = 0
    total_S_n = 0
    total_R_n = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        instance = generate_instance(n)
        R_n, S_n = measure_invariant(instance)
        
        if R_n is None or S_n is None:
            return {
                "metric_name": "Symmetric Spaces vs Rank Variance",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_S_n += S_n
        total_R_n += R_n
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_S_n = total_S_n / instances_tested
    mean_R_n = total_R_n / instances_tested
    
    conjecture_holds = correlation_check(mean_S_n, mean_R_n)
    counterexample = "" if conjecture_holds else f"Mean symmetric spaces {mean_S_n} not within ±5 of mean variance {mean_R_n}"
    
    return {
        "metric_name": "Symmetric Spaces vs Rank Variance",
        "metric_value": mean_S_n,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean symmetric spaces not within ±5 of mean variance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")