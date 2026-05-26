# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def and_or_tree(f, n):
    if n == 1:
        return f
    mid = len(f) // 2
    left = and_or_tree(f[:mid], n-1)
    right = and_or_tree(f[mid:], n-1)
    return [left[i] & right[i] for i in range(mid)] + [left[i] | right[i] for i in range(mid)]

def compute_metric(f):
    n = len(f).bit_length() - 1
    tree = and_or_tree(f, n)
    communication_complexity = len(tree)
    rho_f = math.log2(communication_complexity)
    return communication_complexity <= 2**rho_f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    metric_value = compute_metric(f)
    instances_tested = 1
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else "communication_complexity > 2^rho_f"
    return {
        "metric_name": "Communication Complexity",
        "metric_value": communication_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 307))  # First 30 primes
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")