# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_polynomial(n):
    return [random.randint(0, 1) for _ in range(n + 1)]

def compute_coefficients_sum(f, r, p):
    n = len(f) - 1
    total = 0
    for i in range(n + 1):
        total += f[i] ** r
    return total % p

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_polynomial(n)
        p = random.randint(2, min(100, 2**n))  # Ensure p is a prime number
        
        for r in range(1, n + 1):
            coeff_sum = compute_coefficients_sum(f, r, p)
            if coeff_sum < Fraction(1, p ** r).limit_denominator():
                results.append((f, r, p, False))
                break
        else:
            results.append((f, None, p, True))
    
    metric_value = sum(1 for _, _, _, holds in results if holds) / len(results)
    conjecture_holds = all(holds for _, _, _, holds in results)
    counterexample = "" if conjecture_holds else f"Failed for polynomial {results[0][0]} with r={results[0][1]}, p={results[0][2]}"
    
    return {
        "metric_name": "Fraction of seeds where conjecture holds",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")