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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    even = fast_walsh_hadamard_transform(f[::2])
    odd = fast_walsh_hadamard_transform(f[1::2])
    result = [0] * n
    for i in range(n // 2):
        result[i] = even[i] + odd[i]
        result[i + n // 2] = even[i] - odd[i]
    return result

def sensitivity(f, n):
    max_sens = 0
    for i in range(n):
        sens = 0
        for x in range(1 << n):
            if (x >> i) & 1:
                continue
            x_i = x ^ (1 << i)
            sens += abs(f[x] - f[x_i])
        max_sens = max(max_sens, sens)
    return max_sens

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(1 << n)]
    
    # Compute Fourier coefficients
    f_hat = fast_walsh_hadamard_transform(f)
    max_fourier_coeff = max(abs(coeff) for coeff in f_hat)
    
    # Calculate sensitivity
    sens = sensitivity(f, n)
    
    # Check the conjecture
    holds = max_fourier_coeff >= sens / math.sqrt(n)
    counterexample = "" if holds else "sensitivity too high"
    
    return {
        "metric_name": "max_fourier_coeff",
        "metric_value": max_fourier_coeff,
        "instances_tested": 1,
        "conjecture_holds": holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37, 41, 43, 47]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"sensitivity too high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")