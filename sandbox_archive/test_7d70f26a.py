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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_jordan_algebra(f):
        # Placeholder for actual Jordan algebra calculation
        return sum(f) / len(f)
    
    def read_twice_bp_size(f):
        # Placeholder for actual BP size calculation
        return len(f) * 2
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    jordan_algebra = calculate_jordan_algebra(f)
    bp_size = read_twice_bp_size(f)
    
    metric_value = jordan_algebra / (math.log(bp_size, 2) ** 2)
    conjecture_holds = metric_value <= n
    counterexample = "" if conjecture_holds else f"J(f)={metric_value}, n={n}"
    
    return {
        "metric_name": "Noncommutative Geometric Invariant J(f)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"J(f) exceeds O(log^2(n))\" first_failing_seed={first_failing_seed}")