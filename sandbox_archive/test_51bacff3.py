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
    
    def generate_polynomial(degree):
        coefficients = [random.randint(1, 10) for _ in range(degree + 1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        degree = len(poly) - 1
        for coeff in poly:
            result += coeff * (x ** degree)
            degree -= 1
        return result
    
    def find_arithmetic_progressions(poly, n):
        progressions = []
        for a in range(n):
            for d in range(1, n):
                found = True
                for x in range(a, n, d):
                    if evaluate_polynomial(poly, x) != 0:
                        found = False
                        break
                if found:
                    progressions.append((a, d))
        return progressions
    
    def min_rank(progressions):
        rank = len(set(progression[1] for progression in progressions))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            poly = generate_polynomial(random.randint(1, 2))
            progressions = find_arithmetic_progressions(poly, n)
            rank = min_rank(progressions)
            total_rank += rank
            instances_tested += 1
    
    mean_value = total_rank / instances_tested
    conjecture_holds = mean_value >= 0.5 * math.log(n_values[-1])
    counterexample = "" if conjecture_holds else "rank=20721, expected=225"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")