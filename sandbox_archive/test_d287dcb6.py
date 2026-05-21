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
from fractions import Fraction
import math

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def evaluate_boolean_function(f, x):
    n = int(math.log2(len(f)))
    result = f[0]
    for i in range(1, n + 1):
        bit = (x >> (n - i)) & 1
        if bit == 1:
            result ^= f[i]
    return result

def count_generators(f):
    n = int(math.log2(len(f)))
    points = []
    for x in range(2**n):
        y = evaluate_boolean_function(f, x)
        points.append((x, y))
    
    # Remove duplicate points
    unique_points = list(set(points))
    
    return len(unique_points)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_generators = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_boolean_function(n)
            generators = count_generators(f)
            total_generators += generators
            instances_tested += 1
    
    mean_generators = Fraction(total_generators, instances_tested)
    conjecture_holds = mean_generators >= Fraction(2**n, 4)
    
    return {
        "metric_name": "mean_generators",
        "metric_value": float(mean_generators),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean generators {mean_generators} < 2^{n}/4"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean generators < 2^n/4\" first_failing_seed={first_failing_seed}")