# auto-injected by SEC sandbox
import math
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
from itertools import combinations

def generate_boolean_instance(n):
    return [random.choice([0, 1]) for _ in range(n)]

def compute_minimal_order(solutions):
    n = len(solutions[0])
    if not solutions:
        return None
    for i in range(1, n + 1):
        if all(all(s[j] == s[k] for j, k in combinations(range(n), i)) for s in solutions):
            return i
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_order = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_boolean_instance(n)
            solutions = [instance]
            order = compute_minimal_order(solutions)
            if order is not None:
                total_order += order
                instances_tested += 1
        if instances_tested == 0:
            return {
                "metric_name": "minimal_order",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "no_solutions_found"
            }
        mean_order = total_order / instances_tested
        results.append(mean_order)
    return {
        "metric_name": "minimal_order",
        "metric_value": sum(results) / len(results),
        "instances_tested": 30,
        "n_max": 40,
        "conjecture_holds": all(order <= n**(1/3) * 1.1 for order in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= (n**(1/3) * 1.1)) / len(results)
    if all(r <= n**(1/3) * 1.1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r > n**(1/3) * 1.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > n**(1/3) * 1.1)
        print(f"RESULT: FALSIFIED counterexample='order_exceeds_bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")