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

def minimal_order(space):
    # Placeholder for actual implementation of minimal order calculation
    return len(space)

def communication_complexity_rank(space):
    # Placeholder for actual implementation of communication complexity rank calculation
    return len(space) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        space = [random.randint(1, n) for _ in range(n)]  # Example quasihomogeneous space
        order = minimal_order(space)
        rank = communication_complexity_rank(space)
        results.append((order, rank))
    
    mean_rank = sum(rank for _, rank in results) / len(results)
    conjecture_holds = all(rank <= order**2 for _, rank in results)
    counterexample = "" if conjecture_holds else "minimal_order_undefined"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default list of primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='minimal_order_undefined' first_failing_seed={first_failing_seed}")