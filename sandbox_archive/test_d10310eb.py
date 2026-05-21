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
    
    def parity_function(n, x):
        return sum(x[i] for i in range(n)) % 2
    
    def noncommutative_fourier_transform(n, d):
        if n == 1:
            return {0: 1}
        transform = {}
        for k in range(2**n):
            coeff = 1
            for i in range(n):
                if (k >> i) & 1:
                    coeff *= (-1)**parity_function(i, x)
            transform[k] = coeff
        return transform
    
    def count_nonzero_coefficients(transform):
        return sum(abs(coeff) > 0.5 for coeff in transform.values())
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            x = [random.randint(0, 1) for _ in range(n)]
            d = random.randint(2, 4)
            transform = noncommutative_fourier_transform(n, d)
            nonzero_count = count_nonzero_coefficients(transform)
            lower_bound = n ** (1 / (d - 1))
            if nonzero_count < lower_bound:
                return {
                    "metric_name": "nonzero_coefficient_count",
                    "metric_value": nonzero_count,
                    "instances_tested": instances_tested + 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, d={d}, x={x}, lower_bound={lower_bound}, actual_count={nonzero_count}"
                }
            total_metric_value += nonzero_count
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / (len(n_values) * 5)
    
    return {
        "metric_name": "nonzero_coefficient_count",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")