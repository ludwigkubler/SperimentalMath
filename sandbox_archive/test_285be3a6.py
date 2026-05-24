# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small size and increase if necessary
    max_n = 40
    min_rank_sum = 0
    resolution_depth_sum = 0
    instances_tested = 0

    while True:
        f = generate_boolean_function(n)
        hodge_structure_rank = compute_hodge_structure_rank(f)
        tseitin_resolution_depth = compute_tseitin_resolution_depth(f)

        if hodge_structure_rank is None or tseitin_resolution_depth is None:
            continue

        min_rank_sum += hodge_structure_rank
        resolution_depth_sum += tseitin_resolution_depth
        instances_tested += 1

        if n == max_n:
            break

        n += 5

    if instances_tested < 30:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    mean_min_rank = min_rank_sum / instances_tested
    mean_resolution_depth = resolution_depth_sum / instances_tested

    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_resolution_depth - mean_min_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": abs(mean_resolution_depth - mean_min_rank) <= 3,
        "counterexample": ""
    }

def generate_boolean_function(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_hodge_structure_rank(f: list) -> Fraction:
    # Placeholder function to simulate Hodge structure rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return Fraction(random.randint(1, n))

def compute_tseitin_resolution_depth(f: list) -> int:
    # Placeholder function to simulate Tseitin resolution depth computation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 2*n)

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")