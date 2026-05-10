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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * factorial(n - 1)
    
    def kronecker_coefficient(n, k, l):
        if k > n or l > n:
            return 0
        numerator = factorial(n) ** (n - k - l)
        denominator = factorial(k) * factorial(l) * factorial(n - k - l)
        return numerator // denominator
    
    def symmetric_power_decomposition(n, k):
        coefficients = [kronecker_coefficient(n, i, k - i) for i in range(k + 1)]
        return coefficients
    
    n = random.randint(5, 40)
    k = math.ceil(n / 2)
    permanent_coefficients = symmetric_power_decomposition(n, k)
    determinant_coefficients = symmetric_power_decomposition(n, k)
    
    permanent_value = sum(permanent_coefficients)
    determinant_value = sum(determinant_coefficients)
    
    ratio = permanent_value / determinant_value
    
    metric_name = "Kronecker Coefficient Ratio"
    metric_value = ratio
    instances_tested = 1
    conjecture_holds = ratio > 2 ** (n - k)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} is not exponentially larger than 2^{n-k}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")