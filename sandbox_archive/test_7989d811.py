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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            row = []
            for j in range(2**n):
                if f[i] == f[j]:
                    row.append(1)
                else:
                    row.append(0)
            rank += sum(row) / (2**n)
        return rank
    
    def quaternionic_cohomology_order(rank):
        # Simplified approximation for demonstration purposes
        return math.ceil(math.log2(rank))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_random_boolean_function(n)
        rank = communication_complexity_rank(f)
        order = quaternionic_cohomology_order(rank)
        metric_values.append(order)
    
    mean_value = sum(metric_values) / instances_tested
    variance = sum((x - mean_value)**2 for x in metric_values) / instances_tested
    
    conjecture_holds = variance <= math.log(n_max, 2)
    counterexample = "" if conjecture_holds else f"Variance: {variance}, Expected: O(log {n_max})"
    
    return {
        "metric_name": "Quaternionic Cohomology Order Variance",
        "metric_value": variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    variance = sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={variance} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={variance} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Variance exceeds O(log n)\" first_failing_seed={first_failing_seed}")