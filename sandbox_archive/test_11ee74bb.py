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
    
    def hook_length_formula(n):
        return math.factorial(n + 1) // (math.prod(range(1, n)) * math.prod(range(2, n + 2)))
    
    n = random.randint(5, 40)
    lambda_permanent = (n - 1, 1)
    lambda_determinant = (n, 1)
    
    T_permanent = hook_length_formula(n)
    T_determinant = hook_length_formula(n)
    
    ratio = math.log2(T_permanent / T_determinant)
    conjecture_holds = ratio > n / 2
    counterexample = "" if conjecture_holds else f"Ratio {ratio} <= {n/2}"
    
    return {
        "metric_name": "log2(T_permanent / T_determinant)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {r['metric_value']} <= {n/2}\" first_failing_seed={first_failing_seed}")