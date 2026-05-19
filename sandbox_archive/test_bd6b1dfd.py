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
    
    def generate_unit_vector(n):
        vector = [random.gauss(0, 1) for _ in range(n)]
        norm = sum(x**2 for x in vector)**0.5
        return [x / norm for x in vector]
    
    def inner_product(v1, v2):
        return sum(x * y for x, y in zip(v1, v2))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_discrepancy = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 pairs of unit vectors per n
            v1 = generate_unit_vector(n)
            v2 = generate_unit_vector(n)
            product = inner_product(v1, v2)
            total_discrepancy += abs(product)
            instances_tested += 1
    
    mean_discrepancy = total_discrepancy / instances_tested
    lower_bound = math.sqrt(math.log(n))
    
    conjecture_holds = mean_discrepancy >= lower_bound
    counterexample = "" if conjecture_holds else f"mean_discrepancy={mean_discrepancy}, lower_bound={lower_bound}"
    
    return {
        "metric_name": "discrepancy",
        "metric_value": mean_discrepancy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")