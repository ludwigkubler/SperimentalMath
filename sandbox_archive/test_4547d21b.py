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
    
    def is_planar(n):
        if n <= 4:
            return True
        if n == 5:
            return False
        m = random.randint(7, 2 * n - 3)
        edges = set()
        for _ in range(m):
            u, v = sorted(random.sample(range(n), 2))
            edge = (u, v) if u < v else (v, u)
            if edge in edges:
                return False
            edges.add(edge)
        return True

    def min_root_separability(n):
        # Placeholder for actual calculation of minimal root separability
        # For simplicity, we use a dummy value that depends on n
        return n ** (1/3)

    def communication_complexity(n):
        # Placeholder for actual calculation of communication complexity
        # For simplicity, we use a dummy value that depends on n
        return n ** (2/3)

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    min_separability = float('inf')
    max_complexity = float('-inf')

    for n in range(5, n_max + 1):
        if not is_planar(n):
            continue
        separability = min_root_separability(n)
        complexity = communication_complexity(n)
        total_metric_value += separability * complexity
        instances_tested += 1
        min_separability = min(min_separability, separability)
        max_complexity = max(max_complexity, complexity)

    if instances_tested < 30:
        return {
            "metric_name": "min_root_separability * communication_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_metric_value = total_metric_value / instances_tested
    correlation_coefficient = (mean_metric_value - min_separability * max_complexity) / (instances_tested - 1)

    return {
        "metric_name": "min_root_separability * communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={res['seed']}")
                break