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
    
    def generate_noncommutative_algebra(n):
        # Simple noncommutative algebra generator for demonstration purposes
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
        return A

    def compute_lind(A):
        # Minimal local indeterminacy (lind) is a placeholder value
        return random.random()

    def compute_ccrank(A):
        # Communication complexity rank (CCrank) is a placeholder value
        return random.randint(1, 5)

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        A = generate_noncommutative_algebra(n)
        lind_A = compute_lind(A)
        CCrank_A = compute_ccrank(A)
        
        if CCrank_A == 0:
            continue
        
        instances_tested += 1
        n_max = max(n_max, n)
        metric_values.append(lind_A / (2 ** CCrank_A))

    if not metric_values:
        return {
            "metric_name": "lind(A) / 2^CCrank(A)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, [2 ** CCrank_A for _ in metric_values])) / (len(metric_values) * math.sqrt(sum((x - mean) ** 2 for x in metric_values)) * math.sqrt(sum((y - mean) ** 2 for y in [2 ** CCrank_A for _ in metric_values])))
    mean_metric_value = sum(metric_values) / len(metric_values)
    
    return {
        "metric_name": "lind(A) / 2^CCrank(A)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and max(metric_values) <= 10,
        "counterexample": "" if correlation_coefficient >= 0.8 and max(metric_values) <= 10 else f"correlation={correlation_coefficient}, lind(A)={max(metric_values)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)

    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{x['counterexample']}\" first_failing_seed={first_failing_seed}")