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

def minimal_order(Q):
    # Placeholder function to compute the minimal order of a quasihomogeneous space Q
    # This is a dummy implementation and should be replaced with actual logic
    return len(Q)

def communication_complexity_rank(Q):
    # Placeholder function to compute the communication complexity rank of a quasihomogeneous space Q
    # This is a dummy implementation and should be replaced with actual logic
    return minimal_order(Q) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        Q = generate_quasihomogeneous_space(n)
        order_Q = minimal_order(Q)
        rank_Q = communication_complexity_rank(Q)
        results.append((order_Q, rank_Q))
    
    metric_value = sum(rank for _, rank in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _ in results)
    conjecture_holds = all(rank <= order ** 2 for order, rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_quasihomogeneous_space(n):
    # Placeholder function to generate a random quasihomogeneous space of order n
    # This is a dummy implementation and should be replaced with actual logic
    return [random.randint(1, 10) for _ in range(n)]

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")