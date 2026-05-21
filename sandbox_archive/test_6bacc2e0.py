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
    
    n = 10  # Start with a small value and increase if needed
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncommutative_fourier_coefficient(f, λ):
        F_λ_f = sum(f[i] * math.exp(-2j * math.pi * i * λ) for i in range(2**n)) / (2**n)
        return abs(F_λ_f.real)  # Only consider the magnitude of the real part
    
    def communication_complexity(n):
        return n  # Greater-Than function has O(n) communication complexity
    
    f = generate_random_boolean_function(n)
    λ = random.randint(0, n - 1)  # Choose a random irreducible representation
    F_λ_f = noncommutative_fourier_coefficient(f, λ)
    CC_GT_n = communication_complexity(n)
    
    metric_value = F_λ_f / CC_GT_n
    
    return {
        "metric_name": "Noncommutative Fourier Coefficient Inversion",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True if metric_value >= math.log(n) else False,
        "counterexample": "" if metric_value >= math.log(n) else f"Counterexample for n={n}, λ={λ}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")