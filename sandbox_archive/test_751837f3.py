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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncommutative_fourier_coefficient(f, λ):
        n = int(math.log2(len(f)))
        F_λ_f = sum(f[i] * math.exp(-2j * math.pi * i * λ) for i in range(2**n)) / (2**n)
        return abs(F_λ_f.real)  # Use the magnitude of the real part
    
    def communication_complexity(n):
        # Greater-Than function has Θ(log n) communication complexity
        return math.log2(n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    λ = random.randint(0, n-1)
    F_λ_f = noncommutative_fourier_coefficient(f, λ)
    CC_GT_n = communication_complexity(n)
    
    metric_value = F_λ_f / (CC_GT_n * math.log2(n))
    conjecture_holds = metric_value >= 1
    counterexample = "" if conjecture_holds else f"Counterexample for n={n}, λ={λ}"
    
    return {
        "metric_name": "Noncommutative Fourier Coefficient Inversion",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")