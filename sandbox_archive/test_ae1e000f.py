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
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = lambda x: sum(x[i] for i in range(n)) % 2  # Example function
    ft = fourier_transform(f, n)
    
    max_coefficient = max(abs(coeff) for coeff in ft)
    conjecture_holds = max_coefficient < 1 / math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Max coefficient: {max_coefficient}"
    
    return {
        "metric_name": "max_fourier_coefficient",
        "metric_value": max_coefficient,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def fourier_transform(f, n):
    result = [0] * (1 << n)
    for S in range(1 << n):
        sum_val = 0
        for x in range(1 << n):
            term = f(x) * math.exp(-2j * math.pi * S * x / (1 << n))
            sum_val += term
        result[S] = sum_val / math.sqrt(1 << n)
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")