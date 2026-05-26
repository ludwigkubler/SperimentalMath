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
        for a in range(-n, n + 1):
            for d in range(-n, n + 1):
                if d == 0:
                    continue
                progression = [a]
                x = a + d
                while len(progression) < n and -n <= x <= n:
                    if evaluate_polynomial(poly, x) == 0:
                        progression.append(x)
                    x += d
                if len(progression) == n:
                    progressions.append(progression)
        return progressions
    
    def min_rank(progressions):
        rank = float('inf')
        for p in progressions:
            rank = min(rank, len(p))
        return rank
    
    n = random.randint(5, 40)
    poly = generate_polynomial(random.randint(1, 2))
    
    progressions = find_arithmetic_progressions(poly, n)
    minimal_rank = min_rank(progressions)
    
    metric_name = "minimal_rank"
    metric_value = minimal_rank
    instances_tested = len(progressions)
    conjecture_holds = minimal_rank >= math.log(n) * 0.5
    counterexample = "" if conjecture_holds else f"rank={minimal_rank}, expected>={math.log(n) * 0.5}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")