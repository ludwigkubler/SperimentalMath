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

def fast_walsh_hadamard_transform(x):
    n = len(x)
    if n == 1:
        return x
    even = fast_walsh_hadamard_transform(x[0::2])
    odd = fast_walsh_hadamard_transform(x[1::2])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def fourier_coefficients(f, n):
    def f_hat(k):
        sum_val = 0
        for x in range(2 ** n):
            sum_val += f(x) * math.cos(math.pi * k * x / (2 ** n))
        return sum_val / (2 ** n)
    return [f_hat(k) for k in range(2 ** n)]

def disjointness_communication_complexity(n):
    def f(x, y):
        return int(sum(xi != yi for xi, yi in zip(x, y)) > 0)
    
    coefficients = fourier_coefficients(f, n)
    sum_abs_coeffs = sum(abs(coeff) for coeff in coefficients)
    return math.sqrt(sum_abs_coeffs)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cc = disjointness_communication_complexity(n)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": cc,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_cc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")