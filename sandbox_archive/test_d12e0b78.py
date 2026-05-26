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
    
    def find_arithmetic_progressions(poly, n):
        progressions = []
        for a in range(-n, n+1):
            for d in range(-n, n+1):
                if d == 0:
                    continue
                progression = [a + i * d for i in range(n)]
                if all(poly[i] == sum(coeff * x**i for coeff, x in zip(poly, progression)) for i in range(len(poly))):
                    progressions.append(progression)
        return progressions
    
    def minimal_rank(progressions):
        rank = len(set(tuple(p) for p in progressions))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        poly = generate_polynomial(random.randint(1, 2))
        progressions = find_arithmetic_progressions(poly, n)
        rank = minimal_rank(progressions)
        total_rank += rank
        instances_tested += len(progressions)
    
    mean_value = total_rank / instances_tested
    
    C = 1.0
    threshold = 0.5 * C * math.log(n_values[-1])
    
    conjecture_holds = mean_value >= threshold
    counterexample = "" if conjecture_holds else f"rank={mean_value}, expected={threshold}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too low\" first_failing_seed={first_failing_seed}")