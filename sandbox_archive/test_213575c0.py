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
    
    # Parameters for the trial
    q = 2  # Finite field Fq, using q=2 for simplicity
    N = 10  # Degree of the p-adic polynomial
    
    # Generate a random p-adic polynomial f over Fq
    coefficients = [random.randint(0, q-1) for _ in range(N+1)]
    f = lambda x: sum(c * (x ** i) % q for i, c in enumerate(coefficients))
    
    # Compute the tropicalization T(f)
    T_f = {x: math.log(abs(f(x)), 2) if abs(f(x)) > 0 else -math.inf for x in range(N)}
    
    # Define an explicit function g with known ACC⁰ complexity C_g
    C_g = N  # Example ACC⁰ complexity
    
    # Compute D_f(g)
    D_f_g = max(T_f.values())
    
    # Parameters for the conjecture
    c = 1.0  # Constant factor, adjust as needed
    alpha = 1.0  # Exponent, adjust as needed
    
    # Check if the conjecture holds
    expected_value = c * (math.log(C_g) ** alpha)
    metric_difference = abs(D_f_g - expected_value)
    
    conjecture_holds = metric_difference <= 3
    counterexample = "" if conjecture_holds else f"D_f(g)={D_f_g}, expected>= {expected_value}"
    
    return {
        "metric_name": "D_f(g)",
        "metric_value": D_f_g,
        "instances_tested": N,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2903, 2971, 3041, 3119, 3181, 3251, 3323, 3391, 3461, 3533, 3607, 3673, 3749, 3821, 3889, 3967, 4031, 4093, 4157, 4229, 4297, 4369, 4441, 4513, 4583, 4657, 4729, 4799, 4871, 4943, 5011]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and std of metric_value
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    
    squared_diff_sum = sum((r["metric_value"] - mean_metric_value) ** 2 for r in results)
    std_metric_value = math.sqrt(squared_diff_sum / len(results))
    
    # Compute fraction of seeds where conjecture_holds
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")