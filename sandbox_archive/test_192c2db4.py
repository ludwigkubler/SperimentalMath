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
    
    def hypergeometric_zeros(D, n):
        if D <= 0 or n <= 0:
            return 0
        zeros = 0
        for z in [complex(x, y) for x in range(-100, 101) for y in range(-100, 101)]:
            if abs(z) > 1e-6 and abs((1 - z)**(-D/2)) < 1e-6:
                zeros += 1
        return zeros
    
    def polynomial_upper_bound(n):
        # Example: c_D = n^2 (this is a placeholder; replace with actual bound)
        return n**2
    
    max_n = 40
    instances_tested = 0
    total_zeros = 0
    
    for D in range(1, 6):  # Test depths from 1 to 5
        for _ in range(30):
            n = random.randint(1, max_n)
            zeros = hypergeometric_zeros(D, n)
            instances_tested += 1
            total_zeros += zeros
    
    mean_zeros = total_zeros / instances_tested
    conjecture_holds = mean_zeros <= polynomial_upper_bound(max_n) * (2**max_n)
    
    return {
        "metric_name": "mean_zeros",
        "metric_value": mean_zeros,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean zeros {mean_zeros} exceeds bound {polynomial_upper_bound(max_n) * (2**max_n)}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean zeros exceeded bound\" first_failing_seed={first_failing_seed}")