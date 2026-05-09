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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(matrix, shape):
    n = len(shape)
    numerator = 1
    denominator = 1
    for row in range(n):
        for col in range(n):
            hook_length = (n - row) + (n - col) - 1
            numerator *= factorial(hook_length)
            denominator *= matrix[row][col]
    return Fraction(numerator, denominator)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        matrix = [[random.randint(1, n) for _ in range(n)] for _ in range(n)]
        rectangular_shape = (n,) * n
        staircase_shape = tuple(range(n, 0, -1))
        
        rect_count = hook_length_formula(matrix, rectangular_shape)
        stair_count = hook_length_formula(matrix, staircase_shape)
        
        ratio = rect_count / stair_count
        
        if ratio < 2**n:
            conjecture_holds = False
            counterexample = f"Matrix with n={n} failed. Ratio: {ratio}"
            break
        
        instances_tested += 1

    return {
        "metric_name": "Young Tableaux Ratio",
        "metric_value": 2**n,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")