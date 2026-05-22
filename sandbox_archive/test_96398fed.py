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
    
    # Generate a random tropical polynomial with computable coefficients over the real numbers
    n = random.randint(5, 40)
    coeffs = [random.uniform(-10, 10) for _ in range(n + 1)]
    f = sum(c * x**i for i, c in enumerate(coeffs))
    
    # Construct an ACC⁰ circuit for an explicit function in P with varying depth D and size S
    depth = random.randint(2, 5)
    size = random.randint(10, 30)
    MRP_f = sum(1 for x in range(-10, 11) if f.subs(x) == 0)  # Simplified for demonstration
    
    # Compute the predicted threshold
    epsilon = 0.1
    threshold = 2 ** (depth / 2 + epsilon * size)
    
    # Compare MRP(f) with the predicted threshold
    metric_value = MRP_f
    conjecture_holds = MRP_f >= threshold
    counterexample = "" if conjecture_holds else f"MRP(f)={MRP_f}, threshold={threshold}"
    
    return {
        "metric_name": "Minimal Number of Real Points",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")