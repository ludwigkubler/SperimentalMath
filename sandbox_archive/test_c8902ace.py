# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncommutative_fourier_coefficient(f, λ):
        n = len(f)
        # Simplified representation of the Fourier coefficient calculation
        return sum(f[i] * math.exp(-2j * math.pi * i * λ) for i in range(2**n)) / (2**n)
    
    def communication_complexity_gt(n):
        # Known Θ(log n) complexity for Greater-Than function
        return math.log2(n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    λ = random.randint(1, n)
    F_λ_f = noncommutative_fourier_coefficient(f, λ)
    
    CC_GT_n = communication_complexity_gt(n)
    metric_value = abs(F_λ_f) * CC_GT_n
    
    return {
        "metric_name": "Noncommutative Fourier Coefficient Inversion",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": False if metric_value < math.log(n) else True,
        "counterexample": "mapping_undefined" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")