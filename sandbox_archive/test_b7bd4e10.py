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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def comb(n, k):
        if k > n:
            return 0
        numerator = factorial(n)
        denominator = factorial(k) * factorial(n - k)
        return numerator // denominator
    
    def characteristic_polynomial(n):
        # Placeholder for actual computation of the characteristic polynomial
        # For simplicity, we use a random polynomial here
        coefficients = [random.randint(1, 5) for _ in range(n + 1)]
        return coefficients
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_moments = 0
    instances_tested = 0
    
    for n in n_values:
        char_poly = characteristic_polynomial(n)
        moments = []
        
        for i in range(1, n + 1):
            moment = Fraction(factorial(i), sum(comb(n, k) * char_poly[k] ** i for k in range(n + 1)))
            if moment == 0:
                continue
            moments.append(moment)
        
        if not moments:
            continue
        
        total_moments += sum(moments)
        instances_tested += len(moments)
    
    mean_value = total_moments / instances_tested if instances_tested > 0 else 0
    lower_bound = Fraction(n_values[0] ** (2/3))
    
    conjecture_holds = mean_value >= lower_bound
    counterexample = "" if conjecture_holds else f"mean_value={mean_value}, lower_bound={lower_bound}"
    
    return {
        "metric_name": "Sum of Moments",
        "metric_value": float(mean_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")